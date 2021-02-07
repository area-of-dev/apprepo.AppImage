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
import pty
import subprocess

import hexdi

from .mixins import AppImageDesktopMixin
from .mixins import AppImageIconMixin
from .mixins import AppImagePermissionMixin
from .patcher import EqualsSpaceRemover


class AppImageIntegrator(AppImagePermissionMixin, AppImageDesktopMixin, AppImageIconMixin):

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

        desktop = self.desktop(mountpoint)
        if not os.path.exists(desktop) or not os.path.isfile(desktop):
            raise Exception('.desktop file not found for: {}'.format(mountpoint))

        icon = self.icon(mountpoint)
        if not os.path.exists(icon) or not os.path.isfile(icon):
            raise Exception('icon file not found for: {}'.format(icon))

        logger.debug('config: {}'.format(desktop))
        desktopreader.read(desktop)

        desktopreader.set('Desktop Entry', 'Icon', appimage.icon)
        if not desktopreader.has_option('Desktop Entry', 'Version'):
            desktopreader.set('Desktop Entry', 'Version', 1.0)

        for section in desktopreader.sections():
            if desktopreader.has_option(section, 'Exec'):
                exec = desktopreader.get(section, 'Exec')
                exec = desktopreader.replace(exec, appimage.path)
                desktopreader.set(section, 'Exec', exec)

            if desktopreader.has_option(section, 'TryExec'):
                tryexec = desktopreader.get(section, 'TryExec')
                tryexec = desktopreader.replace(tryexec, appimage.path)
                desktopreader.set(section, 'TryExec', tryexec)

        with open(appimage.desktop, 'w') as stream:
            desktopreader.write(EqualsSpaceRemover(stream))

        with open(icon, 'rb') as stream_origin:
            with open(appimage.icon, 'wb') as stream_pending:
                stream_pending.write(stream_origin.read())
                stream_pending.close()
            stream_origin.close()

        if os.path.exists(appimage.path):
            if os.path.exists(appimage.alias):
                os.unlink(appimage.alias)
            os.symlink(appimage.path, appimage.alias)

        process.terminate()

        return appimage
