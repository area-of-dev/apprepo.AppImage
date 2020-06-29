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
from pathlib import Path
import inject


@inject.params(appimagetool='appimagetool', apprepo='apprepo', console='console')
def main(options=None, args=None, appimagetool=None, apprepo=None, console=None):
    search = ' '.join(args).strip('\'" ')

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
        collection_remote[result['package']] = result['hash']

    for appimage, desktop, icon, alias in appimagetool.collection():
        package = os.path.basename(appimage)
        yield '[checking]: {}'.format(package)

        try:

            if package not in collection_remote.keys():
                yield '[ignoring]: {}, unknown package'.format(package)
                continue

            hash_remote = collection_remote[package]
            if not hash_remote: raise ValueError('{}: empty remote hash'.format(package))

            hash_local = get_hash(appimage)
            if not hash_remote: raise ValueError('{}: empty local hash'.format(package))

            if hash_remote == hash_local:
                yield '[ignoring]: {}, up to date'.format(package)
                continue

            for entity in console.install(options, [package]):
                yield entity
        except Exception as ex:
            yield "[error]: {}".format(ex)

    return 0
