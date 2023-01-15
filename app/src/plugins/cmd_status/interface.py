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

import hexdi

from modules.cmd import console


@console.task(name=['status', 'stat'], description="""
display a list of all available AppImage files.
Default locations are /Applications | ~/Applications.
""")
@hexdi.inject('appimagetool')
def main(options=None, args=None, appimagetool=None):
    for appimage in appimagetool.collection():
        yield console.green("[found]: {}, {}, {}, {}".format(
            os.path.basename(appimage.path) if os.path.exists(appimage.path) else "---",
            os.path.basename(appimage.desktop) if os.path.exists(appimage.desktop) else "---",
            os.path.basename(appimage.icon) if glob.glob(appimage.icon) else "---",
            os.path.basename(appimage.alias) if os.path.exists(appimage.alias) else "---",
        ))
