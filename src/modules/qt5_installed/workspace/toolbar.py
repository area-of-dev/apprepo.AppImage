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

from .button import PictureButtonFlat


class ToolbarWidget(QtWidgets.QFrame):
    removeAction = QtCore.pyqtSignal(object)
    startAction = QtCore.pyqtSignal(object)
    infoAction = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(ToolbarWidget, self).__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.remove = PictureButtonFlat('icons/remove')
        self.remove.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        self.remove.clicked.connect(lambda x: self.removeAction.emit(entity))
        self.layout().addWidget(self.remove)

        self.remove = PictureButtonFlat('icons/test')
        self.remove.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        self.remove.clicked.connect(lambda x: self.removeAction.emit(entity))
        self.layout().addWidget(self.remove)

        self.remove = PictureButtonFlat('icons/start')
        self.remove.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        self.remove.clicked.connect(lambda x: self.removeAction.emit(entity))
        self.layout().addWidget(self.remove)

    def setEntity(self, entity):
        self.entity = entity

    def close(self):
        super().deleteLater()
        return super().close()
