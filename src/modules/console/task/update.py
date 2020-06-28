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

    collection_local = {}
    for appimage, desktop, icon, alias in appimagetool.collection():
        yield '[checking]: {}'.format(os.path.basename(appimage))
        collection_local[os.path.basename(appimage)] = get_hash(appimage)

    for package in collection_local.keys():
        yield '[updating]: {}'.format(package)
        if package not in collection_remote.keys():
            continue

        hash_local = collection_local[package]
        hash_remote = collection_remote[package]
        if hash_remote == hash_local:
            continue

        for entity in console.install(options, [Path(package).stem]):
            yield entity

    return 0
