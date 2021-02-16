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

import hexdi

from .cache.interface import AppRepoCache
from .downloader import ServiceDownloader
from .rest import ServiceApprepo


@hexdi.permanent('apprepo')
class ServiceApprepoInstance(ServiceApprepo):
    @hexdi.inject('config')
    def __init__(self, config):
        url = config.get('api.url', 'https://apprepo.de/rest/api')
        return super(ServiceApprepoInstance, self).__init__(url)


@hexdi.permanent('apprepo.hasher')
def hash_provider():
    def get_hash(path, block_size=1024 * 1024):
        hash = hashlib.sha1()
        with open(path, 'rb') as stream:
            while True:
                data = stream.read(block_size)
                if not data: break
                hash.update(data)
        return hash.hexdigest()

    return get_hash


@hexdi.permanent('apprepo.downloader')
class ServiceDownloaderinstance(ServiceDownloader):
    pass


@hexdi.permanent('apprepo.cache')
class ApprepoCacheInstance(AppRepoCache):
    pass
