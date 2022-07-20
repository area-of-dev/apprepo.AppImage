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

import hexdi


@hexdi.inject('appimagetool', 'console')
def integrate(appimage=None, options=False, appimagetool=None, console=None):
    package = os.path.basename(appimage)
    if not package: raise Exception('Package is empty')

    if appimagetool.installed(package, options.systemwide) and not options.force:
        raise Exception('{} already exists, use --force to override it'.format(package))

    appimage = appimagetool.install(
        appimage,
        package,
        options.force,
        options.systemwide
    )

    if not os.path.exists(appimage.desktop): raise Exception('Desktop file is empty')
    if not os.path.exists(appimage.icon): raise Exception('Icon file is empty')
    if not os.path.exists(appimage.alias): raise Exception('Alias file is empty')

    yield console.green("[integrated]: {}".format(appimage.path))
    yield console.green("[integrated]: {}".format(appimage.desktop))
    yield console.green("[integrated]: {}".format(appimage.icon))
    yield console.green("[integrated]: {}".format(appimage.alias))
