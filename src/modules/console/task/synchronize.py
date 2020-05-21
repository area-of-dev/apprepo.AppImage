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
import glob
import inject


@inject.params(config='config', appimagetool='appimagetool', logger='logger')
def main(options=None, args=None, config=None, appimagetool=None, logger=None):
    applications_global = config.get('applications.global', '/Applications')
    applications_global = applications_global.split(':')

    applications_local = config.get('applications.local', '~/Applications')
    applications_local = applications_local.split(':')

    integration = '/usr/share' \
        if options.systemwide else \
        os.path.expanduser('~/.local/share')

    applications = applications_global \
        if options.systemwide else \
        applications_local

    for location in applications:
        location = os.path.expanduser(location)
        if location is None: continue

        for appimage in glob.glob('{}/*.AppImage'.format(location)):
            yield "Application: {}".format(appimage)
            desktop, icon = appimagetool.integrate(appimage, integration)
            yield "\tupdating desktop file: {}".format(desktop)
            yield "\tupdating desktop icon file: {}".format(icon)

    return 0
