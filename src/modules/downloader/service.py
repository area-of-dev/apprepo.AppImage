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
import os
import requests
import tempfile


class ServiceDownloader(object):
    """
    @todo: check for the viruses (?)
    @todo: check signature
    @todo: some other checks
    """

    def download(self, path=None):
        response = requests.get(path)
        if response is None or response.status_code not in [200]:
            raise Exception('Please check your internet connection or try later')

        with tempfile.NamedTemporaryFile(delete=False) as destination:
            destination.write(response.content)
            destination.close()
        return destination.name
