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
from PyQt5 import QtCore


class WorkspaceThread(QtCore.QThread):
    packageAction = QtCore.pyqtSignal(object)
    packageCleanAction = QtCore.pyqtSignal(object)

    groupAction = QtCore.pyqtSignal(object)
    groupCleanAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(WorkspaceThread, self).__init__()
        self.group = None
        self.stop = False

        self.is_pending_packages = True
        self.is_pending_groups = True

    @hexdi.inject('apprepo')
    def _load_groups(self, apprepo):
        self.groupCleanAction.emit(None)
        for entity in apprepo.groups():
            self.groupAction.emit(entity)
            if self.group: continue
            self.group = entity

    @hexdi.inject('apprepo')
    def _load_packages(self, apprepo):
        self.packageCleanAction.emit(None)
        for entity in apprepo.packages_by_group(self.group):
            self.packageAction.emit(entity)

    @hexdi.inject('apprepo')
    def run(self, apprepo):
        while True:
            if self.is_pending_groups:
                self.is_pending_groups = False
                self._load_groups()

            if self.is_pending_packages:
                self.is_pending_packages = False
                self._load_packages()

            if self.stop: break
            QtCore.QThread.msleep(500)

    def groups(self):
        self.is_pending_packages = False
        self.is_pending_groups = True

    def packages(self, group=None):
        self.is_pending_packages = True
        self.is_pending_groups = False
        self.group = group

    def terminate(self) -> None:
        self.stop = True
        super().terminate()
