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


class CommentWidget(QtWidgets.QLabel):
    def __init__(self, text=None):
        super(CommentWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setText(text)

    def close(self):
        super().deleteLater()
        return super().close()


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

        self.entity = entity

        self.install = PictureButtonFlat(QtGui.QIcon('icons/install'))
        self.install.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        self.install.clicked.connect(lambda x: self.actionInstall.emit(self.entity))
        self.layout().addWidget(self.install)

        self.download = PictureButtonFlat(QtGui.QIcon('icons/download'))
        self.download.setToolTip('Download into the "~/Downloads" folder without any system integration')
        self.download.clicked.connect(lambda x: self.actionDownload.emit(self.entity))
        self.layout().addWidget(self.download)

        self.test = PictureButtonFlat(QtGui.QIcon('icons/home'))
        self.test.setToolTip('Go to the application home page')
        self.test.clicked.connect(lambda x: self.actionTest.emit(self.entity))
        self.layout().addWidget(self.test)

        self.test = PictureButtonFlat(QtGui.QIcon('icons/github'))
        self.test.setToolTip('Go to the AppImage package github page')
        self.test.clicked.connect(lambda x: self.actionTest.emit(self.entity))
        self.layout().addWidget(self.test)

        self.test = PictureButtonFlat(QtGui.QIcon('icons/donate'))
        self.test.setToolTip('Support the author of the application')
        self.test.clicked.connect(lambda x: self.actionTest.emit(self.entity))
        self.layout().addWidget(self.test)

        self.test = PictureButtonFlat(QtGui.QIcon('icons/test'))
        self.test.setToolTip('Download into the "~/Downloads" try to start and submit the results to the apprepo')
        self.test.clicked.connect(lambda x: self.actionTest.emit(self.entity))
        self.layout().addWidget(self.test)

    def setEntity(self, entity):
        self.entity = entity

    def close(self):
        super().deleteLater()
        return super().close()


class PreviewNavbarWidget(QtWidgets.QWidget):
    actionBack = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewNavbarWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.back = PictureButtonFlat(QtGui.QIcon('icons/back'))
        self.back.clicked.connect(self.actionBack.emit)
        self.layout().addWidget(self.back)

    def close(self):
        super().deleteLater()
        return super().close()
