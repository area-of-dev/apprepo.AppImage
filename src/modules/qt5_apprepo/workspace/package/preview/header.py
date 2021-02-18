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


class PreviewHeaderWidget(QtWidgets.QWidget):
    actionBack = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewHeaderWidget, self).__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.back = PictureButtonFlat(QtGui.QIcon('icons/sync'))
        self.back.clicked.connect(self.actionBack.emit)
        self.layout().addWidget(self.back)
