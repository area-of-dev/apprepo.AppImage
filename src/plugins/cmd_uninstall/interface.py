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

from modules.cmd import console


@console.task(name=['uninstall', 'remove', 'delete'],
              description="<string>\t- remove the AppImage "
                          "from the system by the name")
@hexdi.inject('appimagetool', 'console.application')
def main(options=None, args=None, appimagetool=None, console=None):
    search = ' '.join(args).strip('\'" ')

    for entity in appimagetool.collection():
        appimage = pathlib.Path(entity.path)
        if appimage is None: continue

        name = appimage.stem
        if name.lower() != search:
            continue

        yield console.green("[removed]: {}, {}, {}, {}".format(
            os.path.basename(entity.path),
            os.path.basename(entity.desktop),
            os.path.basename(entity.icon),
            os.path.basename(entity.alias),
        ))

        for path in glob.glob(entity.path):
            os.remove(path)

        for path in glob.glob(entity.desktop):
            os.remove(path)

        for path in glob.glob(entity.alias):
            os.remove(path)

        for path in glob.glob(entity.icon):
            os.remove(path)
