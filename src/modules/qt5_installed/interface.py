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
from . import actions


@window.workspace(name='Installed', focus=False, position=1)
@hexdi.inject('workspace.installed', 'workspace.actions', 'actions')
def window_workspace(parent, workspace, workspace_actions, actions):
    workspace.validate.connect(actions.validate)
    workspace.remove.connect(actions.remove)
    workspace.start.connect(actions.start)

    workspace.validate.connect(workspace_actions.update)
    workspace.remove.connect(workspace_actions.update)
    workspace.start.connect(workspace_actions.update)

    return workspace


@window.toolbar(name='Installed', focus=False, position=1)
@hexdi.inject('toolbar.installed')
def window_toolbar(parent=None, toolbar=None):
    toolbar.actionUpdate.connect(actions.on_action_update)
    toolbar.actionSynchronize.connect(actions.on_action_synchronize)
    toolbar.actionCleanup.connect(actions.on_action_cleanup)

    parent.actionReload.connect(toolbar.reload)
    return toolbar
