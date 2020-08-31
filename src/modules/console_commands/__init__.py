# Copyright 2018 Alex Woroschilow (alex.woroschilow@gmail.com)
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
from importlib.machinery import SourceFileLoader


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options, args):
        try:
            return options.console
        except AttributeError:
            return True

    def boot(self, options, args):

        def import_submodules(__path__to_here):
            result = []

            for smfile in glob.glob("{}/*.py".format(__path__to_here)):
                module_name = os.path.basename(smfile)
                if module_name == '__init__.py':
                    continue
                command = SourceFileLoader("commands.{}".format(module_name.strip('.py')), smfile)
                result.append(command.load_module())
            return result

        path = '{}/commands'.format(os.path.dirname(os.path.abspath(__file__)))
        return import_submodules(path)
