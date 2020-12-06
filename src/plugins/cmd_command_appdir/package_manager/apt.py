# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

import apt
import apt.progress
import requests
from apt.package import Package
from apt.package import Version


class PackageCandidate(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.url == other.url


def get_packages(packages=[], architecture='amd64,x86_64,noarch'):
    cache = apt.Cache()

    try:
        cache.update()
    except Exception as ex:
        print(ex)

    pool = []
    queued = []

    for name in packages:
        if not cache.has_key(name):
            continue

        package: Package = cache.get(name)
        if not package: continue

        for arch in architecture.split(','):
            version: Version = package.candidate
            if not version or version.architecture != arch:
                continue

            if version in pool:
                continue

            pool.append(version)

    while len(pool):
        version: Version = pool.pop()
        if not version.uri:
            continue

        candidate = PackageCandidate(version.source_name, version.uri)
        if candidate in queued: continue

        queued.append(candidate)

        for dependency in version.dependencies:
            for dependency_version in dependency.target_versions:
                if dependency_version in pool:
                    continue

                for arch in architecture.split(','):
                    if dependency_version.architecture == arch:

                        candidate = PackageCandidate(dependency_version.source_name, dependency_version.uri)
                        if candidate in queued: continue

                        pool.append(dependency_version)
                        continue

    return queued


def download(package=None, destination=None):
    filename = "{}/{}".format(destination, os.path.basename(package.url))
    with requests.get(package.url, stream=True) as stream:
        stream.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)
            file.close()
        return filename

    return None


def unpack(package=None, destination=None):
    os.system("dpkg -x {} {}".format(
        package, destination
    ))
