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
import glob
import os

import inject


@inject.params(appimagetool='appimagetool', logger='logger')
def main(options=None, args=None, appimagetool=None, logger=None):
    profile = os.path.expanduser('~/.profile')
    if not os.path.exists(profile) or not os.path.isfile(profile):
        yield "[notice] ~/.profile does not exist, creating..."
        with open(profile, 'w+') as stream:
            stream.write('PATH=~/.local/bin:$PATH')
            stream.close()

    for appimage, desktop, icon, alias in appimagetool.collection():

        if not os.path.exists(desktop) or not glob.glob(icon) or not os.path.exists(alias):
            desktop, icon, alias = appimagetool.integrate(appimage, options.systemwide)

        yield "[done]: {}, {}, {}, {}".format(
            os.path.basename(appimage)
            if appimage is not None and os.path.exists(appimage)
            else '---',
            os.path.basename(desktop) if
            desktop is not None and os.path.exists(desktop)
            else '---',
            os.path.basename(icon) if
            icon is not None and glob.glob(icon)
            else '---',
            os.path.basename(alias) if
            alias is not None and os.path.exists(alias)
            else '---'
        )

    return 0
