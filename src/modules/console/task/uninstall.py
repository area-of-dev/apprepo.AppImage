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
import os
import pathlib

import inject


@inject.params(appimagetool='appimagetool', logger='logger')
def main(options=None, args=None, appimagetool=None, logger=None):
    search = ' '.join(args).strip('\'" ')
    for appimage, desktop, icon, alias in appimagetool.collection():
        appimage = pathlib.Path(appimage)
        if appimage is None: continue

        appimage_name = appimage.stem
        appimage_name = appimage_name.lower()
        if appimage_name != search:
            continue

        yield "[removed]: {}, {}, {}, {}".format(
            os.path.basename(appimage),
            os.path.basename(desktop),
            os.path.basename(icon),
            os.path.basename(alias),
        )
        os.remove(appimage)
        os.remove(desktop)
        os.remove(icon)
        os.remove(alias)

    return 0
