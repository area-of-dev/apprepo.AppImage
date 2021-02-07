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


class AppImage(object):
    def __init__(self, path):
        self._path = path

    @property
    def systemwide(self):
        return self.path.find('/home') == -1

    @property
    @hexdi.inject('apprepo.desktopreader')
    def name(self, desktopreader):
        desktopreader.read(self.desktop)
        return desktopreader.get('Desktop Entry', 'Name')

    @property
    @hexdi.inject('apprepo.desktopreader')
    def description(self, desktopreader):
        desktopreader.read(self.desktop)
        return desktopreader.get('Desktop Entry', 'Comment')

    @property
    @hexdi.inject('apprepo.desktopreader')
    def categories(self, desktopreader):
        desktopreader.read(self.desktop)
        return desktopreader.get('Desktop Entry', 'Categories')

    @property
    @hexdi.inject('apprepo.integrator')
    def icon(self, integrator):

        icon = "{}/{{}}".format(integrator.icon(self.systemwide))
        icon = icon.format(pathlib.Path(self.path).stem)

        patterns = []
        patterns.append("{}.svg".format(icon))
        patterns.append("{}.png".format(icon))
        patterns.append("{}.xmp".format(icon))
        patterns.append("{}.xpm".format(icon))

        for pattern in patterns:
            for path in glob.glob(pattern):
                return path

        return icon

    @property
    @hexdi.inject('apprepo.integrator')
    def desktop(self, integrator):
        path = "{}/{{}}.desktop".format(integrator.desktop(self.systemwide))
        return path.format(pathlib.Path(self.path).stem)

    @property
    @hexdi.inject('apprepo.integrator')
    def alias(self, integrator):
        path = "{}/{{}}".format(integrator.alias(self.systemwide))
        return path.format(pathlib.Path(self.path).stem.lower())

    @property
    def path(self):
        return self._path

    @property
    def package(self):
        return os.path.basename(self.path)

    @property
    def package_name(self):
        return pathlib.Path(self.path).stem

    def __str__(self):
        return self.path
