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
        yield "Processing: {}".format(desktop)

        config.read(desktop)

        property_exec = config.get('Desktop Entry', 'Exec')
        property_exec = property_exec.split(' ')
        property_exec = property_exec.pop(0)
        if len(property_exec) and os.path.exists(property_exec):
            existed.append(config.get('Desktop Entry', 'Icon'))
            continue

        yield "\tbinary not found, removing..."
        os.remove(desktop)
        continue

    for icon in glob.glob('{}/icons/*'.format(integration)):
        yield "Processing: {}".format(icon)

        icon = pathlib.Path(icon)
        if icon.stem in existed:
            continue

        yield "\t{}.desktop not found, removing...".format(icon.stem)
        os.remove(icon)
        continue

    return 0


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--global", dest="systemwide", help="Apply the changes for all users", action='store_true')
    (options, args) = parser.parse_args()

    try:
        for output in main(options, args):
            print(output)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
