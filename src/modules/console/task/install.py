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
import os
import stat
import json
import requests
import os
import sys
import glob
import optparse


class InstallPackageTask(object):
    def __init__(self, url=None):
        if url is None or not len(url):
            raise Exception('Init url can not be empty')

        self.url = url

    def _permissions(self, systemwide=False):
        if systemwide is None or not systemwide:
            return stat.S_IRWXU
        return stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IRWXO | stat.S_IROTH

    def _destination(self, package, systemwide=False):
        if systemwide is None or not systemwide:
            return os.path.expanduser('~/Applications/{}'.format(package))
        return '/Applications/{}'.format(package)

    def process(self, string=None, replace=False, systemwide=False):
        response = requests.get('{}/{}/'.format(self.url, string))
        if response is None or not response:
            raise Exception('Response object can not be empty')

        if response.status_code not in [200]:
            raise Exception('Please check your internet connection or try later')

        result = json.loads(response.content)

        if 'file' not in result.keys():
            raise Exception('file url not found')

        if 'package' not in result.keys():
            raise Exception('package name not found')

        response = requests.get(result['file'])
        if response is None or not response:
            raise Exception('package name not found')

        if response.status_code not in [200]:
            raise Exception('Please check your internet connection or try later')

        destination = self._destination(result['package'], systemwide)
        if destination is not None and os.path.exists(destination):
            if replace is None or not replace:
                raise Exception('{} already exists, use --force to override t'
                                'he existing package'.format(destination))

        if os.path.exists(destination):
            os.remove(destination)

        destination_folder = os.path.dirname(destination)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder, exist_ok=False)

        with open(destination, 'wb') as stream:
            os.chmod(destination, self._permissions(systemwide))
            stream.write(response.content)
            stream.close()

        return [result]


def main(options=None, args=None):
    yield "not implemented yeat: {}".format(' '.join(args).strip('\'" '))
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
