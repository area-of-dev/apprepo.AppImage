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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .group.list import GroupListWidget
from .package.dashboard import PackageDashboardWidget


class DashboardWidget(QtWidgets.QSplitter):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @hexdi.inject('apprepo.cache')
    def __init__(self, apprepo=None):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.groups = GroupListWidget()
        self.addWidget(self.groups)

        self.packages = PackageDashboardWidget()
        self.packages.setTitle('test')

        self.addWidget(self.packages)

        self.setStretchFactor(0, 2)
        self.setStretchFactor(1, 4)
