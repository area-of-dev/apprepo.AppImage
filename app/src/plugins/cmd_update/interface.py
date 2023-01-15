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


@console.task(name=['update', 'upgrade', 'up'], description="""<string>
Compare the installed applications and the application 
in the repository and install the version from repository
if the differences are present
""")
def update_action(options=None, args=None):
    if args is None or not len(args):
        args = [None]

    
    for package in args:
        package = package.strip('\'"') if package else None
        for output in _update_action(package, options):
            yield output
    return 0


@hexdi.inject('appimagetool', 'apprepo', 'console.application', 'apprepo.hasher')
def _update_action(search=None, options=None, appimagetool=None, apprepo=None, application=None, hasher=None):
    version_remote = {}
    for result in apprepo.search('' if not search else search):

        package = result.get('package', None)
        if not package: continue

        package_hash = result.get('hash', None)
        if not package_hash: continue

        version_remote[package] = package_hash

    for entity in appimagetool.collection(version_remote.keys()):
        yield console.comment('[checking]: {}...'.format(entity.name))

        try:

            package = os.path.basename(entity.path)
            if not package: continue

            if package not in version_remote.keys():
                yield console.warning('[ignoring]: {}, unknown package'.format(package))
                continue

            hash_remote = version_remote[package]
            if not hash_remote: raise ValueError('{}: empty remote hash'.format(package))

            hash_local = hasher(entity.path)
            if not hash_remote: raise ValueError('{}: empty local hash'.format(package))

            if hash_remote == hash_local:
                yield '[{}]: {}, up to date'.format(console.warning('ignoring'), package)
                continue


            options.force = True
            
            command = application.get_command('install')
            for entity in command(options, [package]):
                yield entity

        except Exception as ex:
            yield console.error("[error]: {}".format(console.error(ex)))
            
    yield console.comment('[done]: {}...'.format(search))
