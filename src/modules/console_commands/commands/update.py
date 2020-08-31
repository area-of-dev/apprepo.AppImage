# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
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
import hashlib
import os

import inject

from modules.console import console


@console.task(name=['update', 'upgrade', 'up'], description="Compare the installed applications and the application in the repository and install the version from repository if the differences are present")
@inject.params(appimagetool='appimagetool', apprepo='apprepo', application='console')
def main(options=None, args=None, appimagetool=None, apprepo=None, application=None):
    """

    :param options:
    :param args:
    :param appimagetool:
    :param apprepo:
    :param application:
    :return:
    """

    def get_hash(path, block_size=1024 * 1024):
        md5 = hashlib.md5()
        with open(path, 'rb') as stream:
            while True:
                data = stream.read(block_size)
                if not data: break
                md5.update(data)

            md5.update(stream.read())
        return md5.hexdigest()

    collection_remote = {}
    for result in apprepo.search(''):
        package = result['package']
        if not package: continue

        hash = result['hash']
        if not package: continue

        collection_remote[package] = hash

    for appimage, desktop, icon, alias in appimagetool.collection():
        package = os.path.basename(appimage)
        yield '[{}]: {}'.format(console.blue('checking'), package)

        try:

            if package not in collection_remote.keys():
                yield '[{}]: {}, unknown package'.format(console.warning('ignoring'), package)
                continue

            hash_remote = collection_remote[package]
            if not hash_remote: raise ValueError('{}: empty remote hash'.format(package))

            hash_local = get_hash(appimage)
            if not hash_remote: raise ValueError('{}: empty local hash'.format(package))

            if hash_remote == hash_local:
                yield '[{}]: {}, up to date'.format(console.warning('ignoring'), package)
                continue

            command = application.get_command('install')
            for entity in command(options, [package]):
                yield entity

        except Exception as ex:
            yield "[{}]: {}".format(console.error('error'), console.error(ex))

    return 0
