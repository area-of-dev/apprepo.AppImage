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
import logging
import logging.handlers
import sys

import hexdi


class Application(object):

    def __init__(self, options, args):
        from modules.kernel import kernel
        self.kernel = kernel.Kernel(options, args)

    @hexdi.inject('console.application')
    def run(self, options, args, application):

        logger = logging.getLogger('application')
        logger.info('Console mode, config: {}'.format(options.config))

        try:
            command = application.get_command(args[0] if len(args) else 'help')
            for output in command(options, args[1:]):
                sys.stdout.write("{}\n".format(output))
                sys.stdout.flush()

        except Exception as ex:
            sys.stdout.write("[{}] {}\n".format(application.error('failed'), application.error(ex)))
            sys.stdout.flush()

            loglevel = options.loglevel \
                if isinstance(options.loglevel, int) else \
                options.loglevel.upper()

            if loglevel in [logging.DEBUG, 'DEBUG']:
                raise ex

        except KeyboardInterrupt as ex:
            sys.stdout.write("\n[{}] {}\n".format(application.error('cancelled'), application.error(ex)))
            sys.stdout.flush()
