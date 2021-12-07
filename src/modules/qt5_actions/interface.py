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
@hexdi.inject('workspace.actions', 'thread.actions')
def window_workspace(parent, workspace, thread):
    # thread.packageCleanAction.connect(workspace.cleanPackage)
    # thread.packageAction.connect(workspace.addPackage)
    #
    # workspace.actionPackage.connect(lambda x: print(x))
    # workspace.actionInstall.connect(lambda x: print(x))
    # workspace.actionDownload.connect(lambda x: print(x))
    # workspace.actionRemove.connect(lambda x: print(x))
    # workspace.actionTest.connect(lambda x: print(x))
    # workspace.actionStart.connect(lambda x: print(x))
    thread.start()

    # workspace.validate.connect(workspace.update)
    # workspace.remove.connect(workspace.update)
    # workspace.start.connect(workspace.update)

    return workspace
