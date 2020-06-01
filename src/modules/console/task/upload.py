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
import inject


@inject.params(config='config', apprepo='apprepo')
def main(options=None, args=None, config=None, apprepo=None):
    print(config.get('user.token', 'zMUOyCMZFT24UOsTVWyR'))
    assert (hasattr(options, 'version_token'))
    assert (hasattr(options, 'version_description'))
    assert (hasattr(options, 'version_name'))

    authentication = config.get('user.token', 'zMUOyCMZFT24UOsTVWyR')
    apprepo.upload(args[0], authentication, 'abjtJR9fcuWAzOIn0NMP6sHVmU4gvF3C', '111', 'test')

    yield "[uploading] {}...".format(args[0])

    return 0
