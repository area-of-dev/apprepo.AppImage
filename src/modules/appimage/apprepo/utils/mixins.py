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
import stat


class AppImagePrefixMixin(object):
    def prefix(self, systemwide=False):
        if systemwide: return '/usr'
        return os.path.expanduser('~/.local')


class AppImagePermissionMixin(AppImagePrefixMixin):
    def permissions(self, systemwide=False):
        if not systemwide: return stat.S_IRWXU
        return stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IRWXO | stat.S_IROTH


class AppImageDestinationMixin(AppImagePrefixMixin):
    def destination(self, package, systemwide=False):
        if systemwide: return '/Applications/{}'.format(package)
        return '{}/{}'.format(os.path.expanduser("~/Applications"), package)


class AppImageDesktopMixin(AppImagePrefixMixin):
    def desktop(self, systemwide=False):
        return "{}/share/applications".format(self.prefix(systemwide))

    def desktop_file(self, location):
        for path in glob.glob('{}/*.desktop'.format(location)):
            return path
        return None

    def desktop_origin(self, location):
        return self.desktop_file(location)


class AppImageAliasMixin(AppImagePrefixMixin):
    def alias(self, systemwide=False):
        return "{}/bin".format(self.prefix(systemwide))


class AppImageIconMixin(AppImagePrefixMixin):

    def icon(self, systemwide=False):
        return "{}/share/icons".format(self.prefix(systemwide))

    def icon_file(self, location):
        patterns = []
        patterns.append("{}/*.svg".format(location))
        patterns.append("{}/*.png".format(location))
        patterns.append("{}/*.xmp".format(location))
        patterns.append("{}/*.xpm".format(location))
        for pattern in patterns:
            for path in glob.glob(pattern):
                return path
        return None

    def icon_origin(self, location):
        return self.icon_file(location)
