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
    def _prefix(self):
        if not self.systemwide:
            return os.path.expanduser('~/.local')
        return '/usr'

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
    def icon(self):
        path = pathlib.Path(self.path)
        assert (path is not None)

        icon = '{}/share/icons/{}'.format(self._prefix, path.stem)

        for path in glob.glob("{}.{}".format(icon, 'svg')):
            return path

        for path in glob.glob("{}.{}".format(icon, 'png')):
            return path

        for path in glob.glob("{}.{}".format(icon, 'xpm')):
            return path

        return None

    @property
    def desktop(self):
        path = pathlib.Path(self.path)
        assert (path is not None)

        return '{}/share/applications/{}.desktop'. \
            format(self._prefix, path.stem)

    @property
    def alias(self):
        path = pathlib.Path(self.path)
        assert (path is not None)

        return '{}/bin/{}'.format(
            self._prefix,
            path.stem.lower()
        )

    @property
    def path(self):
        return self._path

    def __str__(self):
        print([
            self.name,
            self.description,
            self.categories,
            self.icon,
            self.desktop,
            self.alias,
        ])
        return self.path
