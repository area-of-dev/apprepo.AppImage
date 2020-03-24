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
import inject


class Console(object):

    def search(self, request=None):
        print('search', request)

    def install(self, collection=[]):
        for word in collection:
            print('install', word)

    def update(self, collection=[]):
        for word in collection:
            print('update', word)

    def remove(self, collection=[]):
        for word in collection:
            print('remove', word)

    def synchronize(self, request=None):
        print('synchronize', request)
