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
import math
import os
import sys

import requests


class ServiceApprepo(object):
    def __init__(self, url=None):
        self.url = url

    def _progressbar(self, progress=None, filesize=None):
        if progress is None: return progress
        if filesize is None: return progress

        done = int(50 * progress / filesize)

        progress_done = '=' * done
        progress_pending = ' ' * (50 - done)
        progress_percent = progress / filesize * 100
        sys.stdout.write("\r[uploading] [{}{}] {:>.1f} %".format(
            progress_done, progress_pending, progress_percent
        ))

        if progress_percent == 100:
            sys.stdout.write('\n')

        sys.stdout.flush()
        return progress

    def groups(self):

        try:
            response = requests.get('{}/package/groups'.format(self.url))
        except Exception as ex:
            return

        if not response: raise Exception('something went wrong, please try later')
        if response.status_code not in [200]: raise Exception('something went wrong, please try later')

        for entity in json.loads(response.content):
            yield entity

    def packages(self):

        try:
            response = requests.get('{}/package'.format(self.url))
        except Exception as ex:
            return

        if not response: raise Exception('something went wrong, please try later')
        if response.status_code not in [200]: raise Exception('something went wrong, please try later')

        for entity in json.loads(response.content):
            yield entity

    def search(self, string=None):

        try:
            response = requests.get('{}/package?search={}'.format(self.url, string))
        except Exception as ex:
            return

        if not response: raise Exception('something went wrong, please try later')
        if response.status_code not in [200]: raise Exception('something went wrong, please try later')

        for package in json.loads(response.content):
            yield package

    def package(self, string=None):

        try:
            response = requests.get('{}/package/{}/'.format(self.url, string))
        except Exception as ex:
            return

        if not response: raise Exception('Can not fetch package data: {}'.format(string))
        if response.status_code not in [200]: raise Exception('Can not fetch package data: {}'.format(string))

        yield json.loads(response.content)

    def package_by_token(self, string=None):

        try:
            response = requests.get('{}/private/package/{}/'.format(self.url, string))
        except Exception as ex:
            return

        if not response: raise Exception('Can not fetch package data: {}'.format(string))
        if response.status_code not in [200]: raise Exception('Can not fetch package data: {}'.format(string))

        return json.loads(response.content)

    def package_ipfs_cid_new(self, authentication=None, token=None, name=None, description=None, ipfs_cid=None,
                             ipfs_gateway=None):
        """

        :param authentication:
        :param token:
        :param name:
        :param description:
        :param ipfs_cid:
        :param ipfs_gateway:
        :return:
        """
        response = requests.post('{}/private/package/version/{}/create/'.format(self.url, token), data={
            'name': name,
            'description': description,
            'hash': ipfs_cid,
            'ipfs_cid': ipfs_cid,
            'ipfs_gateway': ipfs_gateway,
        }, headers={'Authorization': authentication})

        if response is not None and response.status_code not in [200]:
            raise Exception('Repository unreachable')

        if response is not None and response.status_code in [200]:
            return json.loads(response.content)

        raise Exception('Unknown error, please try again later')

    def upload(self, path=None, authentication=None, token=None, name=None, description=None):
        assert (path is not None and len(path))
        assert (os.path.exists(path) and not os.path.isdir(path))

        start = 0
        filesize = os.path.getsize(path)

        with open(path, "rb") as stream:
            unique = None

            maximum = 1024 * 1024
            chunk_count = math.ceil(float(filesize) / maximum)
            chunk_count_sent = 0
            hash_md5 = hashlib.md5()
            hash_sha1 = hashlib.sha1()
            while True:

                end = min(filesize, start + maximum)

                stream.seek(start)
                chunk = stream.read(maximum)
                hash_sha1.update(chunk)
                hash_md5.update(chunk)

                try:
                    response = requests.post('{}/private/package/upload/initialize/'.format(self.url), headers={
                        'Content-Range': 'bytes {}-{}/{}'.format(start, end - 1, filesize),
                        'Authorization': authentication or None
                    }, files={'file': chunk}, data={'upload_id': unique}, )
                except Exception as ex:
                    return

                if not response: raise Exception(response.content)
                if response.status_code not in [200]: raise Exception(response.content)

                self._progressbar(start + len(chunk), filesize)

                start = end

                chunk_count_sent += 1
                details = json.loads(response.content)

                if 'upload_id' not in details.keys(): raise Exception('upload_id not found')

                unique = details.get('upload_id')
                if chunk_count > chunk_count_sent:
                    continue
                break

            try:
                response = requests.post('{}/private/package/upload/complete/finalize/'.format(self.url), data={
                    'sha1': hash_sha1.hexdigest(),
                    'md5': hash_md5.hexdigest(),
                    'token': token or None,
                    'file': os.path.basename(path),
                    'description': description or '',
                    'name': name or '',
                    'upload_id': unique
                }, headers={'Authorization': authentication})
            except Exception as ex:
                return

            details = json.loads(response.content)
            if 'success' not in details.keys(): raise Exception('success not found')
            if 'package' not in details.keys(): raise Exception('package not found')

            return details.get('package')
