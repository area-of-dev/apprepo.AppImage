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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ToolbarButton
from .text import SearchField


class ToolbarWidgetTab(QtWidgets.QWidget):
    actionSearch = QtCore.pyqtSignal(object)
    actionUpdate = QtCore.pyqtSignal(object)

    def __init__(self, themes=None):
        super(ToolbarWidgetTab, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.update = ToolbarButton(self, "Update", QtGui.QIcon('icons/sync'))
        self.update.clicked.connect(self.actionUpdate.emit)
        self.layout().addWidget(self.update)

        self.search = SearchField(self)
        self.search.returnPressed.connect(lambda: self.actionSearch.emit(self.search.text()))
        self.layout().addWidget(self.search, -1)

        self.reload(None)

    @hexdi.inject('config')
    def reload(self, event, config=None):
        pass
