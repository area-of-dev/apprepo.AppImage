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

import hexdi

from modules.qt5 import window


@window.workspace(name='Installed', focus=True, position=0)
@hexdi.inject('workspace.installed')
def window_workspace(parent=None, workspace=None):
    return workspace


@window.toolbar(name='Installed', focus=True, position=0)
@hexdi.inject('toolbar.installed')
def window_toolbar(parent=None, toolbar=None):
    parent.actionReload.connect(toolbar.reload)
    return toolbar
