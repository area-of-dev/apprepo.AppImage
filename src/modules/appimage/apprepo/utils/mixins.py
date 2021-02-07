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
import stat

import hexdi


class AppImagePermissionMixin(object):
    def permissions(self, systemwide=False):
        if not systemwide: return stat.S_IRWXU
        return stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IRWXO | stat.S_IROTH


class AppImageDestinationMixin(object):

    @hexdi.inject('apprepo.integrator')
    def destination(self, package, systemwide=False, integrator=None):
        return '{}/{}'.format(integrator.destination(systemwide), package)


class AppImageDesktopMixin(object):
    def desktop_origin(self, mountpoint):
        for path in glob.glob('{}/*.desktop'.format(mountpoint)):
            return path
        return None


class AppImageIconMixin(object):
    def icon_origin(self, mountpoint):

        patterns = []
        patterns.append("{}/*.svg".format(mountpoint))
        patterns.append("{}/*.png".format(mountpoint))
        patterns.append("{}/*.xmp".format(mountpoint))
        patterns.append("{}/*.xpm".format(mountpoint))
        for pattern in patterns:
            for path in glob.glob(pattern):
                return path
        return None
