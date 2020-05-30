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
import sys
import glob
import configparser
import pathlib
import optparse


def main(options=None, args=None):
    integration = '/usr/share' if options.systemwide else \
        os.path.expanduser('~/.local/share')

    config = configparser.RawConfigParser()
    config.optionxform = str

    existed = []
    for desktop in glob.glob('{}/applications/*.desktop'.format(integration)):
        yield "[found]: {}".format(os.path.basename(desktop))

        desktop_name = pathlib.Path(desktop)
        desktop_name = desktop_name.stem

        config.read(desktop)

        property_exec = config.get('Desktop Entry', 'Exec')
        property_exec = property_exec.split(' ')
        property_exec = property_exec.pop(0)

        property_exec_name = pathlib.Path(property_exec)
        property_exec_name = property_exec_name.stem

        if property_exec_name != desktop_name:
            yield "[removing]: {}, binary name is not the same as the .desktop file name...". \
                format(os.path.basename(desktop))
            os.remove(desktop)
            continue

        if not os.path.exists(property_exec):
            yield "[removing]: {}, binary not found..." \
                .format(os.path.basename(desktop))
            os.remove(desktop)
            continue

        existed.append(config.get('Desktop Entry', 'Icon'))
        continue

    for icon in glob.glob('{}/icons/*'.format(integration)):
        yield "[found]: {}".format(os.path.basename(icon))

        icon = pathlib.Path(icon)
        if icon.stem in existed:
            continue

        yield "[removing]: {}, .desktop file not found..." \
            .format(os.path.basename(icon))

        os.remove(icon)
        continue

    return 0
