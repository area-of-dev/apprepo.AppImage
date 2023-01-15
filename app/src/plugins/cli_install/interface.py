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

import hexdi

from modules.cmd import console
from plugins.cli_install import actions


@console.task(name=['install', 'get', 'in'], description="""<string>
install the application and integrate it into the system
""")
@hexdi.inject('apprepo')
def main(options=None, args=None, apprepo=None):
    string = ' '.join(args).strip('\'" ')
    if not string: raise Exception('search string can not be empty')

    for entity in apprepo.package(string):
        for output in actions.install(entity, options, None):
            yield output
    return 0
