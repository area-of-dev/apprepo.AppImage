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
import glob
import logging
import os
from importlib import util


class Kernel(object):

    def __init__(self, options: {} = None, args: [] = None, sources: [] = ["plugins/**", "modules/**"]):

        logger = logging.getLogger('kernel')
        for module in self._modules(sources, options, args):

            spec_default = util.find_spec('{}.default'.format(module.__name__))
            if spec_default and spec_default.loader:
                logger.debug("loading defaults: {}...".format(module.__name__))
                spec_default.loader.load_module()

            spec_interface = util.find_spec('{}.interface'.format(module.__name__))
            logger.debug("booting: {}".format(module))
            if spec_interface and spec_interface.loader:
                logger.debug("loading interface: {}...".format(module.__name__))
                spec_interface.loader.load_module()

    def _candidates(self, sources: [] = None):
        for mask in sources:
            if not mask:
                continue

            for source in glob.glob(mask):
                if not source:
                    continue

                if not os.path.isdir(source):
                    continue

                yield source.replace('/', '.')

    def _modules(self, sources: [] = None, options: {} = None, args: [] = None):

        modules = []

        logger = logging.getLogger('kernel')
        for source in self._candidates(sources):
            try:

                spec = util.find_spec(source)
                if not spec.loader: continue

                module = spec.loader.load_module()
                if not module: continue
                logger.debug("found: {}".format(module.__name__))

                if hasattr(module, 'enabled'):
                    enabled = getattr(module, 'enabled')
                    if not callable(enabled):
                        continue

                    if not enabled(options, args):
                        continue

                logger.debug("loading: {}..".format(module.__name__))
                modules.append(module)

                spec_service = util.find_spec('{}.service'.format(module.__name__))
                if spec_service and spec_service.loader:
                    logger.debug("loading services: {}...".format(module.__name__))
                    spec_service.loader.load_module()


            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(source, err))
                continue

        return modules
