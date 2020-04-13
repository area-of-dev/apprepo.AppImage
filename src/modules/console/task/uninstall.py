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


class UninstallPackageTask(object):
    def __init__(self, url=None):
        if url is None or not len(url):
            raise Exception('Init url can not be empty')

        self.url = url

    def _destination(self, package, systemwide=False):
        if systemwide is None or not systemwide:
            return os.path.expanduser('~/Applications/{}'.format(package))
        return '/Applications/{}'.format(package)

    def process(self, string=None, options=False):
        response = requests.get('{}/{}/'.format(self.url, string))
        if response is None or not response:
            raise Exception('package "{}" not found'.format(string))

        if response.status_code not in [200]:
            raise Exception('Please check your internet connection or try later')

        result = json.loads(response.content)

        if 'file' not in result.keys():
            raise Exception('file url not found')

        if 'package' not in result.keys():
            raise Exception('package name not found')

        response = requests.get(result['file'])
        if response is None or not response:
            raise Exception('package "{}" not found'.format(string))

        if response.status_code not in [200]:
            raise Exception('Please check your internet connection or try later')

        destination = self._destination(result['package'], options.systemwide)
        if not os.path.exists(destination):
            raise Exception('{} not found'.format(destination))

        if os.path.exists(destination):
            os.remove(destination)

        return [result]
