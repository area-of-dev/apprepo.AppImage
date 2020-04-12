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
import logging
import optparse
import inject

from importlib import util

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

    @inject.params(console='console')
    def exec_(self, options, args, console=None):
        if not len(args): return None

        actionsmap = {
            'find': console.search_package,
            'find-package': console.search_package,
            'search': console.search_package,
            'search-package': console.search_package,
            'find-group': console.search_group,
            'upload': console.upload_version,
            'upload-version': console.upload_version,
            'upload-package': console.upload_version,
            'push-version': console.upload_version,
            'push-package': console.upload_version,
        }

        command = args[0] or None
        if not len(command) or command not in actionsmap.keys():
            raise Exception('unknown command: {}'.format(command))

        action = actionsmap[command] or None
        if action is None or not callable(action):
            raise Exception('command action not defined: {}'.format(command))

        return action(' '.join(args[1:]).strip('\'" '), options)


if __name__ == "__main__":
    parser = optparse.OptionParser()

    logfile = os.path.expanduser('~/.config/AOD-Store/default.log')

    parser.add_option("--logfile", default=logfile, dest="logfile", help="Logfile location")
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    parser.add_option("--version-token", dest="version_token", help="Upload token", default=None)
    parser.add_option("--version-description", dest="version_description", help="description", default=None)
    parser.add_option("--version-name", dest="version_name", help="Upload name", default=None)

    configfile = os.path.expanduser('~/.config/AOD-Store/default.conf')
    parser.add_option("--config", default=configfile, dest="config", help="Config file location")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_(options, args))
