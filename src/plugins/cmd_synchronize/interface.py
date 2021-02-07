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


@console.task(name=['synchronize', 'sync'],
              description="go through all available AppImage files "
                          "and integrate them into the system if necessary")
@hexdi.inject('appimagetool', 'console.application')
def main(options=None, args=None, appimagetool=None, console=None):
    profile = os.path.expanduser('~/.profile')
    if not os.path.exists(profile) or not os.path.isfile(profile):
        yield "[{}] ~/.profile does not exist, creating...".format(console.blue('notice'))
        with open(profile, 'w+') as stream:
            stream.write('PATH=~/.local/bin:$PATH')
            stream.close()

    for index, appimage in enumerate(appimagetool.collection(), start=0):
        if appimage.desktop and appimage.alias and appimage.icon:
            if os.path.exists(appimage.desktop) and \
                    os.path.exists(appimage.alias) and \
                    os.path.exists(appimage.icon):
                continue

        try:
            appimage = appimagetool.integrate(appimage)
            if not appimage: raise ValueError('Integration failed')

            yield console.green("[synchronized]: {}, {}, {}, {}".format(
                os.path.basename(appimage.path) if os.path.exists(appimage.path) else "---",
                os.path.basename(appimage.desktop) if os.path.exists(appimage.desktop) else "---",
                os.path.basename(appimage.icon) if glob.glob(appimage.icon) else "---",
                os.path.basename(appimage.alias) if os.path.exists(appimage.alias) else "---",
            ))

        except Exception as ex:
            yield console.error("[error]: {}, {}".format(
                appimage.path, ex
            ))
