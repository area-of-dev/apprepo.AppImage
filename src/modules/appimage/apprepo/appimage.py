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
from multiprocessing.pool import ThreadPool

import hexdi

from .model import appimage


def get_folder_bin(appdir_root):
    return '{}/bin'.format(appdir_root)


def get_folder_lib(appdir_root):
    return '{}/lib64'.format(appdir_root)


def get_folder_share(appdir_root):
    return '{}/share'.format(appdir_root)


def get_folder_libexec(appdir_root):
    return '{}/libexec'.format(appdir_root)


def get_folder_libpython(appdir_root):
    return '{}/lib64/python'.format(appdir_root)


def get_folder_libqt5(appdir_root):
    return '{}/lib64/qt5'.format(appdir_root)


def get_folder_libperl5(appdir_root):
    yield '{}/lib64/perl'.format(appdir_root)
    yield '{}/lib64/perl-base'.format(appdir_root)
    yield '{}/lib64/perl5'.format(appdir_root)
    yield '{}/share/perl'.format(appdir_root)
    yield '{}/share/perl-base'.format(appdir_root)
    yield '{}/share/perl5'.format(appdir_root)


def shaper(*args, **kwargs):
    priority = kwargs.get('priority', 0)

    @hexdi.inject('appimagetool')
    def wrapper1(*args, **kwargs):
        assert (len(args) > 1)
        factory: AppImageManager = args[1]

        factory.add_shaper((args[0], priority))

        return args[0]

    return wrapper1


def apprun(*args, **kwargs):
    priority = kwargs.get('priority', 0)

    @hexdi.inject('appimagetool')
    def wrapper1(*args, **kwargs):
        assert (len(args) > 1)
        factory: AppImageManager = args[1]

        factory.add_apprun((args[0], priority))

        return args[0]

    return wrapper1


class AppImageManager(object):
    pool = ThreadPool(processes=1)

    def __init__(self, locations=[]):
        self.locations = locations

        self.shapers = []
        self.apprun = []

    def add_shaper(self, callback):
        self.shapers.append(callback)
        return self

    def add_apprun(self, callback):
        self.apprun.append(callback)
        return self

    def get_shapers(self):
        for bunch in sorted(self.shapers, key=lambda tup: tup[1]):
            yield bunch[0]

    def get_appruns(self):
        for bunch in sorted(self.apprun, key=lambda tup: tup[1]):
            yield bunch[0]

    def collection(self, filter=None):
        for index, location in enumerate(self.locations, start=0):
            location = os.path.expanduser(location)
            if location is None: continue

            patterns = ['{}/*.AppImage'.format(location)]
            if filter is not None and len(filter):
                patterns = ['{}/{}'.format(location, x) for x in filter]

            for patten in patterns:
                for path in glob.glob(patten):
                    yield appimage.AppImage(path)

    def check(self, appimage):
        raise Exception('Not implemented')

    def integrate(self, appimage):
        raise Exception('Not implemented')

    def install(self, tempfile, package, force=False, systemwide=False):
        raise Exception('Not implemented')

    def installed(self, package, systemwide=False):
        raise Exception('Not implemented')
