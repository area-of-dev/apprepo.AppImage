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

from modules.cmd import console


@console.task(name=['install', 'get', 'in'],
              description="<string>\tinstall the application "
                          "and integrate it into the system")
@hexdi.inject('appimagetool', 'apprepo', 'apprepo.downloader', 'console')
def main(options=None, args=None, appimagetool=None, apprepo=None, downloader=None, console=None):
    string = ' '.join(args).strip('\'" ')
    if not string: raise Exception('search string can not be empty')

    for entity in apprepo.package(string):

        package = entity.get('package', None)
        if not package: raise Exception('Package is empty')

        if not options.force and appimagetool.installed(package, options.systemwide):
            raise Exception('{} already exists, use --force to override it'.format(package))

        download_file = entity.get('file', None)
        if not download_file: raise Exception('File is empty')

        download = downloader.download(download_file)
        if not download: yield 'Can not download: {}'.format(download_file)

        assert (os.path.exists(download))

        appimage = appimagetool.install(
            download, package,
            options.force,
            options.systemwide
        )

        if not os.path.exists(appimage.desktop): raise Exception('Desktop file is empty')
        if not os.path.exists(appimage.icon): raise Exception('Icon file is empty')
        if not os.path.exists(appimage.alias): raise Exception('Alias file is empty')

        yield console.green("[done]: {}, {}, {}, {}".format(
            os.path.basename(appimage.path)     if os.path.exists(appimage.path)    else "---",
            os.path.basename(appimage.desktop)  if os.path.exists(appimage.desktop) else "---",
            os.path.basename(appimage.icon)     if os.path.exists(appimage.icon)    else "---",
            os.path.basename(appimage.alias)    if os.path.exists(appimage.alias)   else "---",
        ))

    return 0
