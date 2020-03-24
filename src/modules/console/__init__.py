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
import inject

from .service import Console


class Loader(object):
    console = Console()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def boot(self, options, args):
        if not len(args): return None

        if args[0] in ['search', 'lookup', 'se']:
            return self.console.search(args[1:])

        if args[0] in ['install', 'download', 'get', 'in']:
            return self.console.install(args[1:])

        if args[0] in ['update', 'refresh', 'up']:
            return self.console.update(args[1:])

        if args[0] in ['remove', 'delete', 'del', 'rm']:
            return self.console.remove(args[1:])

        if args[0] in ['synchronize', 'actualize', 'sync']:
            return self.console.synchronize(args[1:])
