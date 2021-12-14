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
import os

import hexdi


@hexdi.inject('appimagetool', 'console.application')
def remove(search=None, options=None, appimagetool=None, console=None):
    for entity in appimagetool.collection([search]):
        yield console.comment("[removing]: {}...".format(
            os.path.basename(entity.path),
        ))

        for path in glob.glob(entity.path):
            os.remove(path)

        for path in glob.glob(entity.desktop):
            os.remove(path)

        for path in glob.glob(entity.alias):
            os.remove(path)

        for path in glob.glob(entity.icon):
            os.remove(path)

        yield console.green("[removed]: {}".format(entity.path))
        yield console.green("[removed]: {}".format(entity.desktop))
        yield console.green("[removed]: {}".format(entity.icon))
        yield console.green("[removed]: {}".format(entity.alias))
