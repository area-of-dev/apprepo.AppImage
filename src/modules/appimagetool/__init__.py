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
import inject


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def __construct(self, config=None):
        from .service import ServiceAppImage

        applications_global = config.get('applications.global', '/Applications')
        applications_global = applications_global.split(':')

        applications_local = config.get('applications.local', '~/Applications')
        applications_local = applications_local.split(':')

        return ServiceAppImage(applications_local, applications_global)

    def configure(self, binder, options, args):
        binder.bind_to_constructor('appimagetool', self.__construct)
