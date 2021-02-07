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

from .mixins import AppImageDesktopMixin
from .mixins import AppImageIconMixin
from .mixins import AppImagePermissionMixin


class AppImageChecker(AppImagePermissionMixin, AppImageDesktopMixin, AppImageIconMixin):
    def check(self, appimage):

        logger = logging.getLogger('appimagetool')
        if not os.path.exists(appimage.path): raise Exception('File does not exist')
        if not os.path.isfile(appimage.path): raise Exception('File does not exist')

        logger.debug('processing: {}'.format(appimage.path))
        if not os.access(appimage.path, os.X_OK):
            os.chmod(appimage.path, self.permissions(appimage.systemwide))

        out_r, out_w = pty.openpty()
        process = subprocess.Popen([appimage.path, '--appimage-mount'], stdout=out_w, stderr=subprocess.PIPE)
        mountpoint = str(os.read(out_r, 2048), 'utf-8', errors='ignore')
        mountpoint = mountpoint.strip("\n\r")

        desktop = self.desktop(mountpoint)
        if not os.path.exists(desktop):
            process.terminate()
            return False

        icon = self.icon(mountpoint)
        if not os.path.exists(icon):
            process.terminate()
            return False

        process.terminate()
        return True
