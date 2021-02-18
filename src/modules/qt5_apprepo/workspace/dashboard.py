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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .group.list import GroupListWidget
from .package.dashboard import PackageDashboardWidget


class DashboardWidget(QtWidgets.QSplitter):
    packageAction = QtCore.pyqtSignal(object)
    groupAction = QtCore.pyqtSignal(object)
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.groups = GroupListWidget()
        self.groups.actionClick.connect(self.groupAction.emit)
        self.addWidget(self.groups)

        self.packages = PackageDashboardWidget()
        self.groups.actionClick.connect(self.packages.onActionDashboard)
        self.packages.actionInstall.connect(self.actionInstall.emit)
        self.packages.actionDownload.connect(self.actionDownload.emit)
        self.packages.actionRemove.connect(self.actionRemove.emit)
        self.packages.actionTest.connect(self.actionTest.emit)
        self.packages.actionStart.connect(self.actionStart.emit)
        self.packages.actionClick.connect(self.packageAction.emit)
        self.addWidget(self.packages)

        self.setStretchFactor(0, 2)
        self.setStretchFactor(1, 4)

    def addPackage(self, entity=None):
        self.packages.addPackage(entity)

    def cleanPackage(self, entity=None):
        self.packages.clean(entity)

    def addGroup(self, entity=None):
        self.groups.addGroup(entity)

    def cleanGroup(self, entity=None):
        self.groups.clean(entity)
