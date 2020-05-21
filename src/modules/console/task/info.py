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


@inject.params(config='config', appimagetool='appimagetool', logger='logger')
def main(options=None, args=None, config=None, appimagetool=None, logger=None):
    applications_global = config.get('applications.global', '/Applications')
    applications_global = applications_global.split(':')

    applications_local = config.get('applications.local', '~/Applications')
    applications_local = applications_local.split(':')

    for appimage in appimagetool.find(applications_global + applications_local):
        yield "Application: {}".format(appimage)

    return 0
