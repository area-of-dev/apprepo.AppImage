# -*- coding: utf-8 -*-
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
import hexdi

from .apprepo import appimage
from .apprepo.utils.checker import AppImageChecker
from .apprepo.utils.installer import AppImageInstaller
from .apprepo.utils.integrator import AppImageIntegrator
from .apprepo.utils.patcher import DesktopFileReader
from .cache.interface import AppImageCache


@hexdi.permanent('appimage')
def appimage_provider():
    from .apprepo import appimage
    return appimage


@hexdi.permanent('appimagetool')
class AppImageManagerInstance(appimage.AppImageManager):
    @hexdi.inject('config')
    def __init__(self, config):
        locations_global = config.get('applications.global', '/Applications')
        locations_local = config.get('applications.local', '~/Applications')

        locations = locations_global.split(':') + locations_local.split(':')
        return super(AppImageManagerInstance, self).__init__(locations)

    @hexdi.inject('apprepo.checker')
    def check(self, appimage, checker=None):
        return self.pool.apply_async(checker.check, (
            appimage,
        )).get()

    @hexdi.inject('apprepo.integrator')
    def integrate(self, appimage, integrator=None):
        return self.pool.apply_async(integrator.integrate, (
            appimage,
        )).get()

    @hexdi.inject('apprepo.installer')
    def install(self, tempfile, package, force=False, systemwide=False, installer=None):
        return self.integrate(self.pool.apply_async(installer.install, (
            tempfile, package, force, systemwide
        )).get())

    @hexdi.inject('apprepo.installer')
    def installed(self, package, systemwide=False, installer=None):
        return installer.installed(package, systemwide)


@hexdi.permanent('apprepo.desktopreader')
class DesktopFileReaderInstance(DesktopFileReader):
    pass


@hexdi.permanent('apprepo.integrator')
class AppImageIntegratorInstance(AppImageIntegrator):
    pass


@hexdi.permanent('apprepo.installer')
class AppImageInstallerInstance(AppImageInstaller):
    pass


@hexdi.permanent('apprepo.checker')
class AppImageCheckerInstance(AppImageChecker):
    pass


@hexdi.permanent('appimage.cache')
class AppImageCacheInstance(AppImageCache):
    pass
