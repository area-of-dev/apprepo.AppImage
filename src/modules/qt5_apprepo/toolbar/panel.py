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
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ToolbarButton
from .image import ImageWidget
from .text import SearchField


class ApprepoToolbarWidget(QtWidgets.QWidget):
    actionSearch = QtCore.pyqtSignal(object)
    actionUpdate = QtCore.pyqtSignal(object)

    def __init__(self, themes=None):
        super(ApprepoToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.layout().addWidget(ImageWidget('icons/logo', 150))

        # self.update = ToolbarButton(self, "aprepo.me", QtGui.QIcon('icons/home'))
        # self.update.clicked.connect(self.actionUpdate.emit)
        # self.layout().addWidget(self.update)
        #
        # self.update = ToolbarButton(self, "github.com", QtGui.QIcon('icons/github'))
        # self.update.clicked.connect(self.actionUpdate.emit)
        # self.layout().addWidget(self.update)

        # spacer = QtWidgets.QWidget()
        # spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.layout().addWidget(spacer)

        motto = QtWidgets.QLabel("The home of the high-quality linux Apps.")
        motto.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        motto.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        motto.setWordWrap(True)
        self.layout().addWidget(motto)

        self.search = SearchField(self)
        self.search.returnPressed.connect(lambda: self.actionSearch.emit(self.search.text()))
        self.layout().addWidget(self.search, -1)


        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.search)
        shortcut.activatedAmbiguously.connect(self.search.setFocus)
        shortcut.activated.connect(self.search.setFocus)
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.search)
        shortcut.activated.connect(lambda event=None: self.search.setText(None))
        shortcut.activatedAmbiguously.connect(self.search.clearFocus)
        shortcut.activated.connect(self.search.clearFocus)

        self.reload(None)

    @hexdi.inject('config')
    def reload(self, event, config=None):
        pass
