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
import hashlib
import json
import os

import math
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

    def upload(self, path=None, authentication=None, token=None, name=None, description=None):
        assert (path is not None and len(path))
        assert (os.path.exists(path) and not os.path.isdir(path))

        start = 0
        size = os.path.getsize(path)

        with open(path, "rb") as stream:
            unique = None

            maximum = 1024 * 1024
            chunk_count = math.ceil(float(size) / maximum)
            chunk_count_sent = 0
            md5 = hashlib.md5()
            while True:

                end = min(size, start + maximum)

                stream.seek(start)
                chunk = stream.read(maximum)
                md5.update(chunk)

                response = requests.post('{}/package/upload/initialize/'.format(self.url), headers={
                    'Content-Range': 'bytes {}-{}/{}'.format(start, end - 1, size),
                    'Authorization': authentication or None
                }, files={'file': chunk}, data={'upload_id': unique}, )

                if response.status_code not in [200]:
                    raise Exception(response.content)

                start = end

                chunk_count_sent += 1
                details = json.loads(response.content)

                if 'upload_id' not in details.keys():
                    raise Exception('upload_id not found')

                unique = details['upload_id']
                if chunk_count > chunk_count_sent:
                    continue
                break

            response = requests.post('{}/package/upload/complete/finalize/'.format(self.url), data={
                'token': token or None,
                'file': os.path.basename(path),
                'description': description or '',
                'name': name or '',
                'upload_id': unique,
                'md5': md5.hexdigest()
            }, headers={'Authorization': authentication})

            details = json.loads(response.content)
            if 'success' not in details.keys():
                raise Exception('success not found')
            if 'package' not in details.keys():
                raise Exception('package not found')
            return details['package']
