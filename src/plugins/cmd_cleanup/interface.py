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


@console.task(name=['cleanup', 'clear'], description="Remove abandoned .desktop files and icons")
@hexdi.inject('appimagetool', 'apprepo.integrator', 'apprepo.desktopreader')
def main(options=None, args=None, appimagetool=None, integrator=None, desktopreader=None):
    appimages = []
    for appimage in appimagetool.collection():
        appimages.append(appimage.package)

    icons = []
    destination = integrator.desktop(options.systemwide)
    for desktop in glob.glob('{}/*.desktop'.format(destination)):
        yield console.comment("[processing]: {}".format(desktop))
        if os.path.isdir(desktop):
            continue

        try:
            desktopreader.read(desktop)

            appimage = desktopreader.get_first('Desktop Entry', 'Exec')
            yield console.comment("[appimage]: {}".format(appimage))

            if not os.path.exists(appimage):
                yield console.warning("[removing]: {} not found".format(appimage))
                os.remove(desktop)
                continue

            desktop_name = pathlib.Path(desktop)
            if not desktop_name: continue

            appimage_name = pathlib.Path(appimage)
            if not appimage_name: continue

            yield console.comment("[name]: {}.desktop".format(desktop_name.stem))
            yield console.comment("[name]: {}.AppImage".format(appimage_name.stem))
            if desktop_name.stem != appimage_name.stem:
                yield console.warning("[removing]: {} wrong naming".format(desktop_name.stem))
                os.remove(desktop)
                continue

            icon = desktopreader.get_first('Desktop Entry', 'Icon')
            yield console.comment("[name]: {}.(svg|png|xmp)".format(icon))
            yield console.green("[clean]: {}".format(desktop))

            icons.append(icon)

        except Exception as ex:
            yield console.error("[exception]: {}...".format(ex))
            continue

    destination = integrator.icon(options.systemwide)
    for icon in glob.glob('{}/*'.format(destination)):
        yield console.comment("[processing]: {}".format(icon))
        if os.path.isdir(icon):
            continue

        icon = pathlib.Path(icon)
        if not icon: continue

        if icon.stem in icons:
            yield console.green("[clean]: {}".format(icon))
            continue

        yield console.warning("[removing]: {}, .desktop file not found...".format(icon))
        os.remove(icon)
