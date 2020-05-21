# -*- coding: utf-8 -*-
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
import json
import requests


class ServiceApprepo(object):
    def __init__(self, url=None):
        self.url = url

    def search(self, string=None):
        response = requests.get('{}/package?search={}'.format(self.url, string))
        if response is None or response.status_code not in [200]:
            raise Exception('something went wrong, please try later')

        for package in json.loads(response.content):
            yield package

    def package(self, string=None):
        response = requests.get('{}/package/{}/'.format(self.url, string))
        if response is None or response.status_code not in [200]:
            raise Exception('Can not fetch package data: {}'.format(string))
        yield json.loads(response.content)
