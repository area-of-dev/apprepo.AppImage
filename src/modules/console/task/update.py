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
import glob
import hashlib
import json
import optparse
import os
import sys
import pathlib

import inject
import requests


class SynchronizePackageTask(object):
    def __init__(self, url=None):
        if url is None or not len(url):
            raise Exception('Init url can not be empty')

        self.url = url

    def _destination(self, systemwide=False):
        if systemwide is None or not systemwide:
            return os.path.expanduser('~/Applications')
        return '/Applications'

    def _hash(self, path, block_size=1024 * 1024):
        md5 = hashlib.md5()
        with open(path, 'rb') as stream:
            while True:
                data = stream.read(block_size)
                if not data: break
                md5.update(data)
        return md5.hexdigest()

    def process(self, string=None, options=None):
        response = requests.get('{}/?search={}'.format(self.url, string))
        if response is None or not response:
            raise Exception('Response object can not be empty')

        if response.status_code not in [200]:
            raise Exception('something went wrong')

        hashmap = {}

        for package in json.loads(response.content):
            hashmap[package['package']] = package

        for path in glob.glob('{}/*.AppImage'.format(self._destination(options.systemwide))):
            basename = os.path.basename(path)
            if basename not in hashmap.keys():
                if not options.cleanup:
                    continue

                if options.force:
                    os.remove(path)

                yield {
                    'name': None,
                    'package': os.path.basename(path),
                    'version': None,
                    'file': None,
                    'slug': None,
                }
                continue

            package_remote = hashmap[basename]
            if 'hash' not in package_remote.keys():
                yield package_remote
                continue

            hash_remote = package_remote['hash']
            if hash_remote is None or not len(hash_remote):
                continue

            hash_current = self._hash(path)
            if hash_remote == hash_current:
                continue

            yield package_remote


@inject.params(appimagetool='appimagetool', apprepo='apprepo', downloader='downloader')
def main(options=None, args=None, appimagetool=None, apprepo=None, downloader=None):
    search = ' '.join(args).strip('\'" ')

    for appimage in appimagetool.list():
        appimage = pathlib.Path(appimage)
        if appimage is None: continue

        appimage_name = appimage.stem
        appimage_name = appimage_name.lower()
        if len(search) and appimage_name != search:
            continue

        yield "Processing: {}...".format(appimage)
        for entity in apprepo.package(appimage_name):
            assert ('package' in entity.keys())
            assert ('file' in entity.keys())

            temp_file = downloader.download(entity['file'])
            if temp_file is None or not len(temp_file):
                yield 'Can not download: {}'.format(entity['file'])
            #
            # assert (os.path.exists(temp_file))
            #
            # appimage, desktop, icon = appimagetool.install(temp_file, entity['package'], options.force,
            #                                                options.systemwide)
            # if desktop is None or icon is None or not len(desktop) or not len(icon):
            #     raise Exception('Can not install, desktop or icon file is empty')
            #
            # yield "Installed: {}".format(appimage)
            # yield "\tdesktop file: {}".format(desktop)
            # yield "\tdesktop icon file: {}".format(icon)

    #
    #     task = SynchronizePackageTask('{}/package'.format(self.api))
    #     for entity in task.process(string, options):
    #         assert ('name' in entity.keys())
    #         assert ('package' in entity.keys())
    #         assert ('version' in entity.keys())
    #         assert ('file' in entity.keys())
    #
    #         yield "Found: {:>s} - recognized as {:>s}, latest version: {}, download: {}".format(
    #             entity['package'] or 'Unknown',
    #             entity['name'] or 'Unknown',
    #             entity['version'] or 'Unknown',
    #             entity['file'] or 'Unknown',
    #         )
    #
    #         assert ('slug' in entity.keys())
    #         if entity['slug'] is None: continue
    #         for output in self.install_package(entity['slug'], options):
    #             yield output

    # yield "not implemented yeat: {}".format(' '.join(args).strip('\'" '))
    return 0


if __name__ == "__main__":
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()

    try:
        for output in main(options, args):
            print(output)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
