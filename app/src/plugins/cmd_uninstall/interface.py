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

from modules.cmd import console
from plugins.cmd_uninstall import actions


@console.task(name=['uninstall', 'remove', 'delete'], description="<string>\t- remove the AppImage " "from the system by the name")
def main(options=None, args=None):
    search = ' '.join(args).strip('\'" ')
    if not len(search): raise Exception('Unknown application')

    for output in actions.remove(search, options):
        yield output
