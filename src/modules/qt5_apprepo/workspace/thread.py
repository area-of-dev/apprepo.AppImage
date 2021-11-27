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
import time

import hexdi
from PyQt5 import QtCore


class WorkspaceThread(QtCore.QThread):
    packageAction = QtCore.pyqtSignal(object)
    packageCleanAction = QtCore.pyqtSignal(object)

    groupAction = QtCore.pyqtSignal(object)
    groupCleanAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(WorkspaceThread, self).__init__()
        self.group = None

    @hexdi.inject('apprepo')
    def _load_groups(self, apprepo):
        self.groupCleanAction.emit(None)
        for entity in apprepo.groups():
            self.groupAction.emit(entity)

    @hexdi.inject('apprepo')
    def _load_packages(self, apprepo):
        if not self.group: return

        self.packageCleanAction.emit(None)
        for entity in apprepo.packages_by_group(self.group):
            self.packageAction.emit(entity)

    @hexdi.inject('apprepo')
    def run(self, apprepo):

        if not self.group:
            time.sleep(1)
            self._load_groups()

        if not self.group:
            time.sleep(1)

        self._load_packages()

    def groups(self, priority=QtCore.QThread.NormalPriority):
        super(WorkspaceThread, self).start(priority)
        self.group = None

    def packages(self, group=None, priority=QtCore.QThread.NormalPriority):
        super(WorkspaceThread, self).start(priority)
        self.group = group

    def __del__(self):
        self.wait()
