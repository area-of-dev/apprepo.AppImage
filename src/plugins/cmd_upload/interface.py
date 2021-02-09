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
from modules.appimage.apprepo.model import appimage

@console.task(name=['upload'], description="upload a new version of the AppImage to the apprepo server")
@hexdi.inject('config', 'apprepo', 'appimagetool', 'console.application', 'apprepo.hasher')
def main(options=None, args=None, config=None, apprepo=None, appimagetool=None, console=None, hasher=None):
    authentication = config.get('user.token', None)
    if not authentication: raise Exception('Authentication token is empty')

    assert (hasattr(options, 'version_token'))
    assert (hasattr(options, 'version_description'))
    assert (hasattr(options, 'version_name'))

    source = args[0] or None
    if not source: raise Exception('Please provide a file to upload')
    if not args: raise Exception('AppImage path is empty')

    token = options.version_token,
    if not token: raise Exception('Version token is empty')

    name = options.version_name,
    if not name: raise Exception('Version name is empty')

    if not os.path.exists(source): raise Exception('{} does not exist or is not a file'.format(source))
    if not os.path.isfile(source): raise Exception('{} does not exist or is not a file'.format(source))

    latest = apprepo.package_by_token(options.version_token)
    if not latest: raise Exception('{} package version not found'.format(options.version_token))

    latest_hash = latest.get('hash', None)
    latest_package = latest.get('package', None)

    if latest_hash and len(latest_hash):
        if latest_hash == hasher(source):
            yield console.blue("[skipped] {} this version was already uploaded...".format(latest_package))
            return

    source = appimage.AppImage(source)
    if not options.skip_check and not appimagetool.check(source):
        raise Exception('{} unknown AppImage format'.format(source))

    yield console.comment("[uploading] {}...".format(source))

    apprepo.upload(source.path, authentication, token, name, options.version_description)

    yield console.green("[done] {}...".format(source))
