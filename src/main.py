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
import logging
import optparse
import os
import sys

import hexdi

abspath = sys.argv[0] \
    if len(sys.argv) else \
    os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

from modules.qt5 import application


@hexdi.permanent('optparse')
class OptionParser(optparse.OptionParser):
    def __init__(self):
        super(OptionParser, self).__init__()

        self.add_option("--loglevel", default=logging.INFO, dest="loglevel", help="Logging level")
        self.add_option("--gui", default='qt5', dest="gui", help="Interface type")

        configfile = '~/.config/apprepo/default.conf'
        self.add_option("--config", default=os.path.expanduser(configfile), dest="config",
                        help="Config file location, default: {}".format(configfile))


if __name__ == "__main__":
    parser = hexdi.resolve('optparse')
    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = application.Application(options, args)
    sys.exit(application.exec_(options, args))
