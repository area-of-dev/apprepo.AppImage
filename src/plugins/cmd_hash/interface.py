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
import os

import hexdi

from modules.cmd import console


@console.task(name=['hash'], description="Calculate hash of the given file")
@hexdi.inject('console.application', 'apprepo.hasher')
def main(options=None, args=None, console=None, hasher=None):
    if not len(args): raise Exception('Please provide a file to upload')

    source = args.pop()
    if not source: raise Exception('Please choose a file')

    if not os.path.exists(source): raise Exception('{} does not exist or is not a file'.format(source))
    if not os.path.isfile(source): raise Exception('{} does not exist or is not a file'.format(source))

    yield hasher(source)
