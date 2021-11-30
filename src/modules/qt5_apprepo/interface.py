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
@hexdi.inject('workspace.apprepo', 'thread.apprepo')
def window_workspace(parent, workspace, thread):
    thread.packageCleanAction.connect(workspace.cleanPackage)
    thread.packageAction.connect(workspace.addPackage)

    thread.groupCleanAction.connect(workspace.cleanGroup)
    thread.groupAction.connect(workspace.addGroup)

    workspace.groupAction.connect(thread.packages)
    workspace.packageAction.connect(lambda x: print(x))
    workspace.actionInstall.connect(lambda x: print(x))
    workspace.actionDownload.connect(lambda x: print(x))
    workspace.actionRemove.connect(lambda x: print(x))
    workspace.actionTest.connect(lambda x: print(x))
    workspace.actionStart.connect(lambda x: print(x))

    thread.start()

    return workspace


@window.toolbar(name='Apprepo', focus=True, position=0)
@hexdi.inject('toolbar.apprepo', 'thread.apprepo')
def window_toolbar(parent=None, toolbar=None, thread=None):
    toolbar.actionSearch.connect(lambda x: print(x))
    toolbar.actionSearch.connect(thread.search)

    parent.actionReload.connect(toolbar.reload)
    return toolbar
