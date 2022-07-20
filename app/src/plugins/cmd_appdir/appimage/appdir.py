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
import shutil
import stat

import hexdi


@hexdi.inject('package.manager')
def get_packages(packages=[], arch='x86_64,noarch', package_manager=None):
    return package_manager.get_packages(packages, arch)


@hexdi.inject('package.manager')
def download(package=None, destination=None, package_manager=None):
    return package_manager.download(package, destination)


@hexdi.inject('package.manager')
def unpack(package=None, destination=None, package_manager=None):
    return package_manager.unpack(package, destination)


@hexdi.inject('appimagetool')
def simplify(appdir_root, appdir_build, package_manager=None):
    for shaper in package_manager.get_shapers():
        for source, destination in shaper(appdir_root, appdir_build):
            yield source, destination

    shutil.rmtree(appdir_build, ignore_errors=True)


@hexdi.inject('appimagetool')
def apprun(appdir_root, package_manager=None):
    lines = []
    for appprun in package_manager.get_appruns():
        lines.extend(appprun(appdir_root))
    lines.append("#exec ${APPDIR}/bin/\n")

    apprun = "{}/AppRun".format(appdir_root)
    with open(apprun, "w") as stream:
        stream.write("\n".join(lines))
        stream.close()

        os.chmod(apprun, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    yield "\n".join(lines)
