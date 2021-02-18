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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import PictureButtonFlat
from .button import ToolbarButton


class CommentWidget(QtWidgets.QLabel):
    def __init__(self, text=None):
        super(CommentWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setText(text)


class PreviewToolbarWidget(QtWidgets.QWidget):
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewToolbarWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.entity = None

        self.install = ToolbarButton(self, "Install", QtGui.QIcon('icons/sync'))
        self.install.clicked.connect(lambda x: self.actionInstall.emit(self.entity))
        self.layout().addWidget(self.install)

        self.download = ToolbarButton(self, "Download", QtGui.QIcon('icons/sync'))
        self.download.clicked.connect(lambda x: self.actionDownload.emit(self.entity))
        self.layout().addWidget(self.download)

        self.remove = ToolbarButton(self, "Remove", QtGui.QIcon('icons/sync'))
        self.remove.clicked.connect(lambda x: self.actionRemove.emit(self.entity))
        self.layout().addWidget(self.remove)

        self.start = ToolbarButton(self, "Start", QtGui.QIcon('icons/sync'))
        self.start.clicked.connect(lambda x: self.actionStart.emit(self.entity))
        self.layout().addWidget(self.start)

        self.test = ToolbarButton(self, "Test", QtGui.QIcon('icons/sync'))
        self.test.clicked.connect(lambda x: self.actionTest.emit(self.entity))
        self.layout().addWidget(self.test)

    def setEntity(self, entity):
        self.entity = entity


class PreviewNavbarWidget(QtWidgets.QWidget):
    actionBack = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewNavbarWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.back = PictureButtonFlat(QtGui.QIcon('icons/sync'))
        self.back.clicked.connect(self.actionBack.emit)
        self.layout().addWidget(self.back)
