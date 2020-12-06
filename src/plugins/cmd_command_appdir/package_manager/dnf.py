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

import dnf
import requests


def get_packages(packages=[], arch='x86_64,noarch'):
    base = dnf.Base()
    base.read_all_repos()
    base.fill_sack()

    q = base.sack.query()
    collection = q.available()

    pool = []
    queued = []

    for name in packages:
        for a in arch.split(','):
            for package in collection.filter(name=name, arch=a):
                if package in pool:
                    continue
                pool.append(package)

    while len(pool):
        pkg = pool.pop()
        if pkg in queued:
            continue

        queued.append(pkg)

        for file in pkg.requires:
            for a in arch.split(','):
                for package in collection.filter(provides=file, arch=a):
                    if package in queued:
                        continue

                    if package in pool:
                        continue

                    pool.append(package)
    return queued


def download(package=None, destination=None):
    filename_rpm = "{}/{}.rpm".format(destination, package.__str__())
    with requests.get(package.remote_location(), stream=True) as stream:
        stream.raise_for_status()
        with open(filename_rpm, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)
            file.close()
        return filename_rpm
    return None


def unpack(package=None, destination=None):
    os.system("cd {} && rpm2cpio {} | cpio -idmv".format(
        destination, package
    ))
