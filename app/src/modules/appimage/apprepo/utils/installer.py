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
import shutil

from .mixins import AppImageDestinationMixin
from .mixins import AppImagePermissionMixin
from ..model import appimage


class AppImageInstaller(AppImagePermissionMixin, AppImageDestinationMixin):

    def installed(self, package, systemwide=False):
        destination = self.destination(package, systemwide)
        return os.path.exists(destination)

    def install(self, tempfile, package, force, systemwide):
        destination = self.destination(package, systemwide)
        if self.installed(package, force) and not force:
            raise Exception('{} already exists, use --force to override t'
                            'he existing package'.format(destination))

        if os.path.exists(destination):
            os.remove(destination)

        folder = os.path.dirname(destination)
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=False)

        shutil.move(tempfile, destination)
        os.chmod(destination, self.permissions(systemwide))

        if os.path.exists(tempfile):
            os.unlink(tempfile)

        return appimage.AppImage(destination)
