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
import glob
import os

import inject

from modules.console import console


@console.task(name=['status', 'stat'], description="display a list of all available AppImage files (/Applications | ~/Applications by default)")
@inject.params(appimagetool='appimagetool', logger='logger')
def main(options=None, args=None, appimagetool=None, logger=None):
    for appimage, desktop, icon, alias in appimagetool.collection():
        yield "[{}found{}]: {}, {}, {}, {}".format(
            console.OKGREEN, console.ENDC,
            os.path.basename(appimage) if os.path.exists(appimage) else "---",
            os.path.basename(desktop) if os.path.exists(desktop) else "---",
            os.path.basename(icon) if glob.glob(icon) else "---",
            os.path.basename(alias) if os.path.exists(alias) else "---",
        )

    return 0
