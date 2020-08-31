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
import logging.handlers
import optparse
import os
import sys
import bs4
import pty
import json
import requests
import configparser
import pathlib
import multiprocessing
from importlib import util

import inject

abspath = sys.argv[0] \
    if len(sys.argv) else \
    os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))


class Application(object):

    def __init__(self, options, args):
        spec = util.find_spec('lib.kernel')
        module = spec.loader.load_module()
        if module is None: return None

        self.kernel = module.Kernel(options, args)

    @inject.params(application='console', logger='logger')
    def run(self, options, args, application, logger=None):
        logger.info('Console mode, config: {}'.format(options.config))

        try:
            command = application.get_command(args[0] if len(args) else 'help')
            for output in command(options, args[1:]):
                sys.stdout.write("{}\n".format(output))
                sys.stdout.flush()
        except Exception as ex:
            sys.stdout.write("[failed] {}\n".format(ex))
            sys.stdout.flush()

            loglevel = options.loglevel \
                if isinstance(options.loglevel, int) else \
                options.loglevel.upper()

            if loglevel in [logging.DEBUG, 'DEBUG']:
                raise ex



if __name__ == "__main__":
    configfile = '~/.config/apprepo/default.conf'

    parser = optparse.OptionParser()
    parser.add_option("--loglevel", default=logging.INFO, dest="loglevel", help="Logging level")
    parser.add_option("--force", dest="force", help="Force execution", action='store_true')
    parser.add_option("--global", dest="systemwide", help="Install the application for all users", action='store_true')
    parser.add_option("--cleanup", dest="cleanup", help="Remove unknown packages", action='store_true')
    parser.add_option("--version-token", dest="version_token", help="Upload token", default=None)
    parser.add_option("--version-description", dest="version_description", help="description", default=None)
    parser.add_option("--version-name", dest="version_name", help="Upload name", default=None)
    parser.add_option("--version-skip-check", dest="skip_check", help="Check appimage structure", action='store_true')

    parser.add_option("--config", default=os.path.expanduser(configfile), dest="config",
                      help="Config file location, default: {}".format(configfile))

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format, handlers=[
        logging.handlers.SysLogHandler(address='/dev/log')
    ])

    application = Application(options, args)
    sys.exit(application.run(options, args))
