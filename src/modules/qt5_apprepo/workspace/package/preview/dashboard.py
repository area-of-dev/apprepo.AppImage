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

from .comments import PreviewCommentsWidget
from .pictures import PreviewPicturesWidget
from .toolbar import PreviewNavbarWidget
from .toolbar import PreviewToolbarWidget


class PreviewDashboardWidget(QtWidgets.QWidget):
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)
    actionBack = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewDashboardWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignTop | Qt.AlignBottom)

        self.navbar = PreviewNavbarWidget()
        self.navbar.actionBack.connect(self.actionBack.emit)
        self.layout().addWidget(self.navbar, 0, 0, 2, 1)

        self.pictures = PreviewPicturesWidget()
        self.layout().addWidget(self.pictures, 0, 1)

        self.comments = PreviewCommentsWidget()
        self.layout().addWidget(self.comments, 1, 1)

        self.toolbar = PreviewToolbarWidget()
        self.toolbar.actionInstall.connect(self.actionInstall.emit)
        self.toolbar.actionDownload.connect(self.actionDownload.emit)
        self.toolbar.actionRemove.connect(self.actionRemove.emit)
        self.toolbar.actionTest.connect(self.actionTest.emit)
        self.toolbar.actionStart.connect(self.actionStart.emit)
        self.layout().addWidget(self.toolbar, 0, 2, 2, 1)

    def setPackage(self, entity):
        self.comments.setEntity(entity)
        self.pictures.setEntity(entity)
        self.toolbar.setEntity(entity)
