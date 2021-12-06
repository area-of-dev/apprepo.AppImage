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
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .image import DragAndDropImageWidget
from .text import SearchField


class ApprepoToolbarWidget(QtWidgets.QWidget):
    search = QtCore.pyqtSignal(object)
    drop = QtCore.pyqtSignal(object)

    def __init__(self, themes=None):
        super(ApprepoToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.dragAndDrop = DragAndDropImageWidget('icons/drop', 40)
        self.dragAndDrop.drop.connect(self.drop.emit)
        self.layout().addWidget(self.dragAndDrop)

        self.searchField = SearchField(self)
        self.searchField.search.connect(self.search.emit)
        self.layout().addWidget(self.searchField, -1)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.searchField)
        shortcut.activatedAmbiguously.connect(self.searchField.setFocus)
        shortcut.activated.connect(self.searchField.setFocus)
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.searchField)
        shortcut.activated.connect(lambda event=None: self.searchField.setText(None))
        shortcut.activatedAmbiguously.connect(self.searchField.clearFocus)
        shortcut.activated.connect(self.searchField.clearFocus)

        self.reload(None)

    @hexdi.inject('config')
    def reload(self, event, config=None):
        pass
