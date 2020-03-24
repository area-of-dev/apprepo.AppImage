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
import glob
import logging
import inject
import importlib
import functools
import re


class Kernel(object):

    def __init__(self, options=None, args=None, sources=["plugins/**/__init__.py", "modules/**/__init__.py"]):

        self.modules = self.get_module_collection(sources)

        inject.configure(functools.partial(
            self.configure,
            modules=self.modules,
            options=options,
            args=args
        ))

        logger = logging.getLogger('kernel')
        for module in sorted(self.modules, key=self._sort_by_module_order):
            if not hasattr(module, 'boot'):
                continue

            loader_boot = getattr(module, 'boot')
            if not callable(loader_boot):
                continue

            logger.debug("booting: {}".format(module))
            module.boot(options, args)

    def _sort_by_module_order(self, module):
        """

        :param module:
        :return:
        """
        if not hasattr(module, 'order'):
            return -1
        return module.order

    def _sort_by_module_name(self, text):
        """

        :param text:
        :return:
        """

        def atoi(text):
            return int(text) if text.isdigit() else text

        return [atoi(c) for c in re.split('(\d+)', text)]

    def get_module_candidates(self, sources=None):
        """

        :param sources:
        :return:
        """
        for mask in sources:
            for source in sorted(glob.glob(mask), key=self._sort_by_module_name, reverse=False):
                if not os.path.exists(source):
                    continue

                source = source.replace('/', '.')
                source = source.replace('.py', '')

                yield source

    def get_module_collection(self, sources=None):
        """

        :param sources:
        :return:
        """
        modules = []

        logger = logging.getLogger('kernel')
        for source in self.get_module_candidates(sources):
            try:

                module = importlib.import_module(source, False)
                logger.debug("found: {}".format(source))
                if not hasattr(module, 'Loader'):
                    continue

                module_class = getattr(module, 'Loader')
                with module_class() as loader:

                    if hasattr(loader, 'enabled'):
                        if not loader.enabled:
                            continue

                    logger.debug("loading: {}".format(loader))
                    modules.append(loader)

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(source, err))
                continue

        return modules

    def configure(self, binder, modules, options=None, args=None):
        """

        :param binder:
        :param modules:
        :param options:
        :param args:
        :return:
        """

        logger = logging.getLogger('kernel')
        for module in sorted(modules, key=self._sort_by_module_order):

            try:

                if not hasattr(module, 'configure'):
                    continue

                configure = getattr(module, 'configure')
                if not callable(configure):
                    continue

                logger.debug("configuring: {}".format(module))

                binder.install(functools.partial(
                    module.configure,
                    options=options,
                    args=args
                ))

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(module, err))
                continue

        binder.bind('logger', logging.getLogger('app'))
        binder.bind('kernel', self)
