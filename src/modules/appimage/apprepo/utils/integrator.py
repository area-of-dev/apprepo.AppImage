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
import logging
import os
import pathlib
import pty
import subprocess

import hexdi

from .mixins import AppImageAliasMixin
from .mixins import AppImageDesktopMixin
from .mixins import AppImageDestinationMixin
from .mixins import AppImageIconMixin
from .mixins import AppImagePermissionMixin
from .patcher import EqualsSpaceRemover


class AppImageIntegrator(AppImagePermissionMixin, AppImageAliasMixin, AppImageDesktopMixin,
                         AppImageIconMixin, AppImageDestinationMixin):

    @hexdi.inject('apprepo.desktopreader')
    def integrate(self, appimage, desktopreader=None):
        logger = logging.getLogger('appimagetool')

        if not os.path.exists(appimage.path): raise Exception('File does not exist')
        if not os.path.isfile(appimage.path): raise Exception('File does not exist')

        logger.debug('processing: {}'.format(appimage.path))
        if not os.access(appimage.path, os.X_OK):
            os.chmod(appimage.path, self.permissions(
                appimage.systemwide
            ))

        out_r, out_w = pty.openpty()
        process = subprocess.Popen([appimage.path, '--appimage-mount'], stdout=out_w, stderr=subprocess.PIPE)
        mountpoint = str(os.read(out_r, 2048), 'utf-8', errors='ignore')
        mountpoint = mountpoint.strip("\n\r")

        os.makedirs(os.path.dirname(appimage.desktop), exist_ok=True)
        os.makedirs(os.path.dirname(appimage.icon), exist_ok=True)
        os.makedirs(os.path.dirname(appimage.alias), exist_ok=True)

        desktop = self.desktop_file(mountpoint)
        if not os.path.exists(desktop) or not os.path.isfile(desktop):
            raise Exception('.desktop file not found for: {}'.format(mountpoint))

        icon = self.icon_file(mountpoint)
        if not os.path.exists(icon) or not os.path.isfile(icon):
            raise Exception('icon file not found for: {}'.format(icon))

        desktopreader.read(desktop)

        desktopreader.set('Desktop Entry', 'Icon', appimage.package_name)
        if not desktopreader.has_option('Desktop Entry', 'Version'):
            desktopreader.set('Desktop Entry', 'Version', 1.0)

        for section in desktopreader.sections():
            if desktopreader.has_option(section, 'Exec'):
                binfile = desktopreader.get(section, 'Exec')
                binfile = desktopreader.replace(binfile, appimage.path)
                desktopreader.set(section, 'Exec', binfile)

            if desktopreader.has_option(section, 'TryExec'):
                binfile = desktopreader.get(section, 'TryExec')
                binfile = desktopreader.replace(binfile, appimage.path)
                desktopreader.set(section, 'TryExec', binfile)

        with open(appimage.desktop, 'w') as stream:
            desktopreader.write(EqualsSpaceRemover(stream))

        icon = pathlib.Path(icon)
        with open(icon, 'rb') as stream_source:
            destination = "{}/{{}}{{}}".format(self.icon(appimage.systemwide))
            destination = destination.format(appimage.package_name, icon.suffix)
            with open(destination, 'wb') as stream_destination:
                stream_destination.write(stream_source.read())
                stream_destination.close()
            stream_source.close()

        if os.path.exists(appimage.path):
            if os.path.exists(appimage.alias):
                os.unlink(appimage.alias)
            os.symlink(appimage.path, appimage.alias)

        process.terminate()

        return appimage
