# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
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
import inject


@inject.params(appimagetool='appimagetool', apprepo='apprepo', downloader='downloader')
def main(options=None, args=None, appimagetool=None, apprepo=None, downloader=None):
    string = ' '.join(args).strip('\'" ')
    if string is None or not len(string):
        raise Exception('search string can not be empty')

    for entity in apprepo.package(string):
        assert ('package' in entity.keys())
        assert ('file' in entity.keys())

        temp_file = downloader.download(entity['file'])
        if temp_file is None or not len(temp_file):
            yield 'Can not download: {}'.format(entity['file'])

        assert (os.path.exists(temp_file))

        appimage, desktop, icon = appimagetool.install(temp_file, entity['package'], options.force, options.systemwide)
        if desktop is None or icon is None or not len(desktop) or not len(icon):
            raise Exception('Can not install, desktop or icon file is empty')

        yield "Installed: {}".format(appimage)
        yield "\tdesktop file: {}".format(desktop)
        yield "\tdesktop icon file: {}".format(icon)

    return 0
