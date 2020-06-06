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
import os

import inject


@inject.params(config='config', apprepo='apprepo', appimagetool='appimagetool')
def main(options=None, args=None, config=None, apprepo=None, appimagetool=None):
    assert (hasattr(options, 'version_token'))
    assert (hasattr(options, 'version_description'))
    assert (hasattr(options, 'version_name'))

    source = args[0] or None
    if source is None or not len(source):
        raise Exception('Please provide a file to upload')

    if not os.path.exists(source) or not os.path.isfile(source):
        raise Exception('{} does not exist or is not a file'.format(source))

    if not options.skip_check and not appimagetool.check(source):
        raise Exception('{} is not an AppImage'.format(source))

    if options.version_token is None or not len(options.version_token):
        raise Exception('Version token is empty')

    if options.version_name is None or not len(options.version_name):
        raise Exception('Version name token is empty')

    if args is None or not len(args):
        raise Exception('AppImage path is empty')

    yield "[uploading] {}...".format(source)

    authentication = config.get('user.token', None)
    if authentication is None or not len(authentication):
        raise Exception('Authentication token is empty')

    apprepo.upload(
        source, authentication,
        options.version_token,
        options.version_name,
        options.version_description
    )

    yield "[done] {}...".format(source)

    return 0
