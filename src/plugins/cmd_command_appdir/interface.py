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

import hexdi

from .appimage import appdir

console = hexdi.resolve('console')
if not console: raise Exception('Console service not found')


@console.task(name=['appdir'], description='Build an AppDir by the given package name (names)')
@hexdi.inject('console.application')
def appdir_action(options=None, arguments=None, application=None):
    if not os.path.exists(options.destination):
        raise ValueError('Destination folder is empty')

    if not len(options.arch):
        raise ValueError('Please select architecture')

    name = arguments.pop(0)
    if not name: raise ValueError('Name is empty')

    appdir_root = "{}/{}.AppDir".format(options.destination, name.capitalize())
    if not os.path.exists(appdir_root):
        os.makedirs(appdir_root, exist_ok=True)

    appdir_build = "{}/{}.AppDir/build".format(options.destination, name.capitalize())
    if not os.path.exists(appdir_build):
        os.makedirs(appdir_build, exist_ok=True)

    queued = appdir.get_packages([name] + arguments, options.arch)
    if not queued: raise ValueError('No packages were found')

    downloaded = []
    total = len(queued)
    for index, package in enumerate(queued, start=1):
        yield "downloading: {} from {}, {}".format(index, total, package.__str__())
        filename_rpm = appdir.download(package, appdir_build)
        if not filename_rpm: raise ValueError(package.__str__())

        downloaded.append(filename_rpm)

    total = len(downloaded)
    for index, filename_rpm in enumerate(downloaded, start=1):
        yield "unpacking: {} from {}, {}".format(index, total, filename_rpm)
        appdir.unpack(filename_rpm, appdir_build)

    for source, destination in appdir.simplify(appdir_root, appdir_build):
        yield "moved: to {}\tfrom\t{}".format(destination, source)

    for line in appdir.apprun(appdir_root):
        yield line
