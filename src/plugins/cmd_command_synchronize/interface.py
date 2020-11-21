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

console = hexdi.resolve('console')
if not console: raise Exception('Console service not found')

@console.task(name=['synchronize', 'sync'], description="go through all available AppImage files and integrate them into the system if necessary")
@hexdi.inject('appimagetool', 'console.application')
def main(options=None, args=None, appimagetool=None, console=None):
    profile = os.path.expanduser('~/.profile')
    if not os.path.exists(profile) or not os.path.isfile(profile):
        yield "[{}] ~/.profile does not exist, creating...".format(console.blue('notice'))
        with open(profile, 'w+') as stream:
            stream.write('PATH=~/.local/bin:$PATH')
            stream.close()

    for appimage, desktop, icon, alias in appimagetool.collection():

        if not os.path.exists(desktop) or not glob.glob(icon) or not os.path.exists(alias):
            desktop, icon, alias = appimagetool.integrate(appimage, options.systemwide)

        yield "[{}]: {}, {}, {}, {}".format(
            console.green('done'),
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
