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


@hexdi.inject('appimagetool', 'apprepo.downloader', 'console')
def install(entity=None, options=False, callback=None, appimagetool=None, downloader=None, console=None):
    package = entity.get('package', None)
    if not package: raise Exception('Package is empty')

    if appimagetool.installed(package, options.systemwide) and not options.force:
        raise Exception('{} already exists, use --force to override it'.format(package))

    download_file = entity.get('file', None)
    if not download_file: raise Exception('File is empty')

    download = downloader.download(download_file, callback if callback is not None else None)
    if not download: raise Exception('Can not download: {}'.format(download_file))

    assert (os.path.exists(download))

    appimage = appimagetool.install(
        download, package,
        options.force,
        options.systemwide
    )

    if not os.path.exists(appimage.desktop): raise Exception('Desktop file is empty')
    if not os.path.exists(appimage.icon): raise Exception('Icon file is empty')
    if not os.path.exists(appimage.alias): raise Exception('Alias file is empty')

    yield console.green("[installed]: {}".format(appimage.path))
    yield console.green("[installed]: {}".format(appimage.desktop))
    yield console.green("[installed]: {}".format(appimage.icon))
    yield console.green("[installed]: {}".format(appimage.alias))
