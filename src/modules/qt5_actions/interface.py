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


@window.workspace(name='Actions', focus=False, position=3)
@hexdi.inject('workspace.actions', 'actions')
def window_workspace(parent, workspace, actions):
    workspace_apprepo = hexdi.resolve('workspace.apprepo')
    workspace_apprepo.actionInstall.connect(actions.install)
    workspace_apprepo.actionDownload.connect(actions.download)
    workspace_apprepo.actionRemove.connect(actions.remove)
    workspace_apprepo.actionTest.connect(actions.validate)
    workspace_apprepo.actionStart.connect(actions.start)

    workspace_apprepo.actionInstall.connect(workspace.update)
    workspace_apprepo.actionDownload.connect(workspace.update)
    workspace_apprepo.actionRemove.connect(workspace.update)
    workspace_apprepo.actionTest.connect(workspace.update)
    workspace_apprepo.actionStart.connect(workspace.update)

    thread = hexdi.resolve('thread.actions')
    thread.start()

    return workspace
