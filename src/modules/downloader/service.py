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
import tempfile

import requests


class ServiceDownloader(object):
    """
    @todo: check for the viruses (?)
    @todo: check signature
    @todo: some other checks
    """

    def _download_stream(self, response):

        filesize = response.headers.get('content-length')
        if filesize is None or not len(filesize):
            raise Exception('Content-Length header is empty')

        progress = 0
        total_length = int(filesize)

        destination = tempfile.NamedTemporaryFile(delete=False)
        with open(destination.name, "ab") as stream:
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk: break
                stream.write(chunk)

                progress += len(chunk)
                done = int(50 * progress / total_length)

                progress_done = '=' * done
                progress_pending = ' ' * (50 - done)
                progress_percent = progress / total_length * 100

                sys.stdout.write("\rdownloading: [{}{}] {:>.1f} %".format(
                    progress_done, progress_pending, progress_percent
                ))

                sys.stdout.flush()
            stream.close()

            sys.stdout.write('\n')
            sys.stdout.flush()

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
