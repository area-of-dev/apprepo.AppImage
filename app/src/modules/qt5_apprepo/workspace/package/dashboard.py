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
from PyQt5.QtCore import Qt

from .label import Title
from .list import PackageListWidget
from .preview.dashboard import PreviewDashboardWidget


class PackageDashboardWidget(QtWidgets.QWidget):
    actionClick = QtCore.pyqtSignal(object)
    actionBack = QtCore.pyqtSignal(object)
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PackageDashboardWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.title = Title('...')
        self.layout().addWidget(self.title)

        self.list = PackageListWidget()
        self.list.actionInstall.connect(self.actionInstall.emit)
        self.list.actionDownload.connect(self.actionDownload.emit)
        self.list.actionRemove.connect(self.actionRemove.emit)
        self.list.actionTest.connect(self.actionTest.emit)
        self.list.actionStart.connect(self.actionStart.emit)

        self.list.actionClick.connect(self.actionClick.emit)
        self.list.actionClick.connect(self.onActionPackage)
        self.layout().addWidget(self.list)

        self.preview = PreviewDashboardWidget()
        self.preview.actionBack.connect(self.onActionDashboard)
        self.preview.actionBack.connect(self.actionBack.emit)
        self.preview.actionInstall.connect(self.actionInstall.emit)
        self.preview.actionDownload.connect(self.actionDownload.emit)
        self.preview.actionRemove.connect(self.actionRemove.emit)
        self.preview.actionTest.connect(self.actionTest.emit)
        self.preview.actionStart.connect(self.actionStart.emit)
        self.preview.setVisible(False)
        self.layout().addWidget(self.preview)

    def setTitle(self, text=None):
        if not text: return self
        self.title.setText(text)
        return self

    def addPackage(self, entity):
        self.list.addEntity(entity)

    def onActionDashboard(self, package):
        self.preview.setVisible(False)
        self.list.setVisible(True)

    def onActionPackage(self, package):
        self.list.setVisible(False)
        self.title.setText(package.get('name', None))
        self.preview.setPackage(package)
        self.preview.setVisible(True)

    def clean(self, entity=None):
        self.list.clean(entity)
        return self

    def close(self):
        super().deleteLater()
        return super().close()
