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
import pathlib


class AppImageDesktopFinder(object):
    def __init__(self, appimage, mountpoint=None):
        self.mountpoint = mountpoint
        self.appimage = appimage

    @property
    def origin(self):
        if self.mountpoint is None:
            return None

        pattern = '{}/*.desktop'.format(self.mountpoint)
        for path in glob.glob(pattern):
            return path

    @property
    def wanted(self):
        desktop_wanted = pathlib.Path(self.appimage)
        return desktop_wanted.stem

    def property(self, origin=None):
        properties = origin.split(' ')
        properties[0] = self.appimage
        return ' '.join(properties)

    def files(self, destination=None):
        return (self.origin, "{}/{}.desktop".format(
            destination, self.wanted
        ))
