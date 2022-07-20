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
import glob
import os
import platform

import hexdi


class Theme(object):
    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    @property
    def preview(self):
        return "{}/preview.png".format(self.path)

    @property
    def stylesheet(self):

        system = platform.system().lower()

        stylesheet_current = '{}/{}.qss' \
            .format(self.path, system)

        if os.path.exists(stylesheet_current):
            return open(stylesheet_current).read()

        stylesheet_default = 'css/{}.qss'.format(system)
        if os.path.exists(stylesheet_default):
            return open(stylesheet_default).read()
        return None


class ServiceTheme(object):
    themes = {}

    def __init__(self, source=None):
        if source is None: return source
        for path in source:
            for source in glob.glob("{}/**/*.qss".format(path)):
                name = os.path.basename(os.path.dirname(source))
                self.themes[name] = Theme(os.path.dirname(source), name)

    def get_stylesheets(self):
        return self.themes.values()

    @hexdi.inject('config')
    def get_stylesheet(self, config=None):
        if config is None: return None

        theme_current = config.get('themes.theme', 'light')

        stylesheet_current = 'themes/{}/{}.qss'.format(
            theme_current, platform.system().lower()
        )
        if os.path.exists(stylesheet_current):
            return open(stylesheet_current).read()

        stylesheet_default = 'css/{}.qss'.format(platform.system().lower())
        if os.path.exists(stylesheet_default):
            return open(stylesheet_default).read()
        return None
