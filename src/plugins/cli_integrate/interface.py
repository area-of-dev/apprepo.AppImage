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
from plugins.cli_integrate import actions


@console.task(name=['integrate'], description="<string>\tintegrate the existing AppImage into the system")
def main(options=None, args=None):
    appimage = ' '.join(args).strip('\'" ')
    if not appimage: raise Exception('search string can not be empty')

    appimage = os.path.expanduser(appimage)
    if not os.path.exists(appimage): raise Exception('Does not exist: {}'.format(appimage))

    for output in actions.integrate(appimage, options):
        yield output

    return 0
