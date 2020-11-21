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
import hexdi

from .apprepo.appimage import AppImage


@hexdi.permanent('appimagetool')
class ServiceAppImageInstance(AppImage):
    @hexdi.inject('config')
    def __init__(self, config):
        applications_global = config.get('applications.global', '/Applications')
        applications_global = applications_global.split(':')

        applications_local = config.get('applications.local', '~/Applications')
        applications_local = applications_local.split(':')

        return super(ServiceAppImageInstance, self).__init__(
            applications_local, applications_global
        )
