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
import logging.handlers
import optparse
import hexdi

abspath = sys.argv[0] \
    if len(sys.argv) else \
    os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))


from modules.cmd_application import application


@hexdi.permanent('optparse')
class OptionParser(optparse.OptionParser):
    def __init__(self):
        super(OptionParser, self).__init__()

        self.add_option("--loglevel", default=logging.INFO, dest="loglevel", help="Logging level")
        self.add_option("--force", dest="force", help="Force execution", action='store_true')
        self.add_option("--global", dest="systemwide", help="Install the application for all users", action='store_true')
        self.add_option("--cleanup", dest="cleanup", help="Remove unknown packages", action='store_true')
        self.add_option("--version-token", dest="version_token", help="Upload token", default=None)
        self.add_option("--version-description", dest="version_description", help="description", default=None)
        self.add_option("--version-name", dest="version_name", help="Upload name", default=None)
        self.add_option("--version-skip-check", dest="skip_check", help="Check appimage structure", action='store_true')

        configfile = '~/.config/apprepo/default.conf'
        self.add_option("--config", default=os.path.expanduser(configfile), dest="config",
                          help="Config file location, default: {}".format(configfile))





if __name__ == "__main__":
    configfile = '~/.config/apprepo/default.conf'

    parser = OptionParser()
    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format, handlers=[
        logging.handlers.SysLogHandler(address='/dev/log')
    ])

    application = application.Application(options, args)
    sys.exit(application.run(options, args))
