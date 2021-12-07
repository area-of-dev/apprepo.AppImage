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


@window.workspace(name='Apprepo', focus=True, position=0)
@hexdi.inject('workspace.apprepo', 'thread.apprepo', 'workspace.actions', 'actions')
def window_workspace(parent, workspace, thread, workspace_actions, actions):
    thread.packageCleanAction.connect(workspace.cleanPackage)
    thread.packageAction.connect(workspace.addPackage)

    thread.groupCleanAction.connect(workspace.cleanGroup)
    thread.groupAction.connect(workspace.addGroup)

    workspace.actionGroup.connect(thread.packages)
    workspace.actionInstall.connect(actions.install)
    workspace.actionDownload.connect(actions.download)
    workspace.actionRemove.connect(actions.remove)
    workspace.actionTest.connect(actions.validate)
    workspace.actionStart.connect(actions.start)

    workspace.actionInstall.connect(workspace_actions.update)
    workspace.actionDownload.connect(workspace_actions.update)
    workspace.actionRemove.connect(workspace_actions.update)
    workspace.actionTest.connect(workspace_actions.update)
    workspace.actionStart.connect(workspace_actions.update)

    thread.start()

    return workspace


@window.toolbar(name='Apprepo', focus=True, position=0)
@hexdi.inject('toolbar.apprepo', 'thread.apprepo', 'workspace.actions', 'actions')
def window_toolbar(parent, toolbar, thread, workspace_actions, actions):
    toolbar.search.connect(thread.search)

    toolbar.drop.connect(actions.integrate)
    toolbar.drop.connect(workspace_actions.update)

    parent.actionReload.connect(toolbar.reload)

    return toolbar
