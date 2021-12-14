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
import os

import hexdi
import shutil


@hexdi.inject('apprepo.downloader', 'console')
def download(entity=None, options=False, callback=None, downloader=None, console=None):
    package = entity.get('package', None)
    if not package: raise Exception('Package is empty')

    download_file = entity.get('file', None)
    if not download_file: raise Exception('File is empty')

    download = downloader.download(download_file, callback if callback is not None else None)
    if not download: raise Exception('Can not download: {}'.format(download_file))

    shutil.move(download, os.path.expanduser("~/Downloads/{}".format(package)))
    yield console.green("[downloaded]: {}".format(download))
