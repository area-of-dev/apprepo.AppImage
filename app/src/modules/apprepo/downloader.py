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

from modules.cmd import console


class ServiceDownloader(object):
    def _download_stream(self, response, callback=None):

        filesize = response.headers.get('content-length')
        if filesize is None or not len(filesize):
            raise Exception('Content-Length header is empty')

        progress = 0
        filesize = int(filesize)

        destination = tempfile.NamedTemporaryFile(delete=False)
        with open(destination.name, "ab") as stream:
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk: break
                stream.write(chunk)

                progress += len(chunk)
                if callback is not None and callable(callback):
                    callback(progress, filesize)

                sys.stdout.flush()
            stream.close()

            sys.stdout.write('\n')
            sys.stdout.flush()

            return destination.name

    def _download_file(self, response, callback=None):
        with tempfile.NamedTemporaryFile(delete=False) as destination:
            destination.write(response.content)
            if callable(callback):
                size = len(response.content)
                callback(size, size)
            destination.close()

        return destination.name

    def _download_progress(self, progress, total):
        done = int(50 * progress / total)

        progress_done = '=' * done
        progress_pending = ' ' * (50 - done)
        progress_percent = progress / total * 100

        sys.stdout.write("\r[{}downloading{}]: [{}{}] {:>.1f} %".format(
            console.OKGREEN,
            console.ENDC,
            progress_done,
            progress_pending,
            progress_percent
        ))

    def download(self, path=None, callback=None):
        callback = self._download_progress \
            if not callback else callback

        response = requests.get(path, stream=True)
        if not response: raise Exception('Can not download file: {}'.format(path))

        if response.status_code not in [200]:
            raise Exception('Can not download file: {}'.format(path))

        total_length = response.headers.get('content-length')
        if not total_length or not len(total_length):
            return self._download_file(response, callback)
        return self._download_stream(response, callback)
