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
import json
import requests


class SearchTask(object):
    def __init__(self, url=None):
        if url is None or not len(url):
            raise Exception('Init url can not be empty')

        self.url = url

    def process(self, string=None):
        response = requests.get('{}/?search={}'.format(self.url, string))
        if response is None or not response:
            raise Exception('Response object can not be empty')

        if response.status_code not in [200]:
            raise Exception('something went wrong')

        for package in json.loads(response.content):
            yield package
