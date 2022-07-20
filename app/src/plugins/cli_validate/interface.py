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
from plugins.cli_validate import actions


@console.task(name=['validate', 'check', 'test'], description="Test compatibility of the selected package with the current host")
@hexdi.inject('apprepo', 'console')
def test_search_request(options=None, args=None, apprepo=None, console=None):
    if args is None or not len(args):
        args = [None]

    for package in args:

        search = package.strip('\'"') \
            if package else None

        if search is None:
            continue

        yield console.comment("[processing]: search request {}...".format(search))
        for entity in apprepo.package(search):
            yield console.comment("[validating]: {}...".format(entity.get('package')))
            for output in actions.validate(entity, options, None):
                yield output

    return 0
