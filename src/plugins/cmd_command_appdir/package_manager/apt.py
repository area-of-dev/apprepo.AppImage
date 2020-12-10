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


def _get_version(collection, architecture):
    for version in collection:
        for arch in architecture.split(','):
            if version.architecture == arch:
                yield version
                break


def get_packages(packages=[], architecture='amd64,x86_64,noarch'):
    cache = apt.Cache()

    try:
        cache.update()
    except Exception as ex:
        print(ex)

    pool = []
    queued = {}

    for name in packages:
        if not cache.has_key(name):
            continue

        package: Package = cache.get(name)
        if not package: continue

        for version in _get_version([package.candidate], architecture):
            if version not in pool:
                pool.append(version)

    while len(pool):
        version: Version = pool.pop()
        if not version.downloadable:
            continue

        if version.__str__() in queued.keys():
            continue

        queued[version.__str__()] = PackageCandidate(version.__str__(), version.uri)

        for dependency in version.get_dependencies('Depends'):
            for dependency_version in _get_version(dependency.target_versions, architecture):
                if dependency_version.__str__() not in queued.keys():
                    pool.append(dependency_version)

    return queued.values()


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
