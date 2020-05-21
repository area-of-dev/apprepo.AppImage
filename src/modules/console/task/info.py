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
import optparse


def main(options=None, args=None):
    applications = '/Applications' if options.systemwide else \
        os.path.expanduser('~/Applications')

    for appimage in glob.glob('{}/*.AppImage'.format(applications)):
        yield "Application: {}".format(appimage)

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
