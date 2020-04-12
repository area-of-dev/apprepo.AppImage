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
import math
import json
import hashlib
import requests


class VersionUploadTask(object):
    def __init__(self, url_initialize=None, url_finalize=None):
        if url_initialize is None or not len(url_initialize):
            raise Exception('Init url can not be empty')

        if url_finalize is None or not len(url_finalize):
            raise Exception('Init url can not be empty')

        self.url_initialize = url_initialize
        self.url_finalize = url_finalize

    def upload(self, path=None, options=None):
        assert (path is not None and len(path))
        assert (os.path.exists(path) and not os.path.isdir(path))

        assert ('token' in options.keys())
        assert ('description' in options.keys())
        assert ('name' in options.keys())

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

                file = {'file': chunk}
                data = {'upload_id': unique}
                response = requests.post(self.url_initialize, files=file, data=data, headers={
                    'Content-Range': 'bytes {}-{}/{}'.format(start, end - 1, size)
                })

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

            response = requests.post(self.url_finalize, data={
                'token': options['token'],
                'file': os.path.basename(path),
                'description': options['description'],
                'name': options['name'],
                'upload_id': unique,
                'md5': md5.hexdigest()
            })

            details = json.loads(response.content)
            if 'success' not in details.keys():
                raise Exception('success not found')
            if 'package' not in details.keys():
                raise Exception('package not found')
            return details['package']
