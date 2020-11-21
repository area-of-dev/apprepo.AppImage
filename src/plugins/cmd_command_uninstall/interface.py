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
import pathlib

import hexdi

console = hexdi.resolve('console')
if not console: raise Exception('Console service not found')
description = "<string>\t- remove the AppImage from the system by the name"


@console.task(name=['uninstall', 'remove', 'delete'], description=description)
@hexdi.inject('appimagetool', 'console.application')
def main(options=None, args=None, appimagetool=None, console=None):
    search = ' '.join(args).strip('\'" ')
    for appimage, desktop, icon, alias in appimagetool.collection():
        appimage = pathlib.Path(appimage)
        if appimage is None: continue

        appimage_name = appimage.stem
        appimage_name = appimage_name.lower()
        if appimage_name != search:
            continue

        yield console.green("[removed]: {}, {}, {}, {}".format(
            os.path.basename(appimage),
            os.path.basename(desktop),
            os.path.basename(icon),
            os.path.basename(alias),
        ))

        for path in glob.glob(str(appimage)):
            os.remove(path)

        for path in glob.glob(str(desktop)):
            os.remove(path)

        for path in glob.glob(str(alias)):
            os.remove(path)

        for path in glob.glob(str(icon)):
            os.remove(path)

    return 0
