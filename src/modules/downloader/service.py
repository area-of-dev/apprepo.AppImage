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
import sys
import os
import requests
import tempfile


class ServiceDownloader(object):
    """
    @todo: check for the viruses (?)
    @todo: check signature
    @todo: some other checks
    """

    def _download_stream(self, response):
        with tempfile.NamedTemporaryFile(delete=False) as destination:
            total_length = response.headers.get('content-length')
            if total_length is None or not len(total_length):
                raise Exception('Content-Length header is empty')

            length_delta = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                length_delta += len(data)
                destination.write(response.content)
                done = int(50 * length_delta / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

            destination.close()
            return destination.name

    def _download_file(self, response):
        with tempfile.NamedTemporaryFile(delete=False) as destination:
            destination.write(response.content)
            destination.close()
        return destination.name

    def download(self, path=None):
        response = requests.get(path, stream=True)
        if response is None or response.status_code not in [200]:
            raise Exception('Can not download file: {}'.format(path))
        total_length = response.headers.get('content-length')
        if total_length is not None and len(total_length):
            return self._download_stream(response)
        return self._download_file(response)
