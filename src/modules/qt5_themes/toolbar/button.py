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


class ToolbarButton(QtWidgets.QToolButton):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, theme=None):
        super(ToolbarButton, self).__init__(parent)
        self.clicked.connect(lambda x: self.actionClick.emit(theme))
        self.setCheckable(False)
        self.theme = theme

        if theme.preview:
            pixmap = QtGui.QPixmap(theme.preview)
            pixmap = pixmap.scaledToWidth(90)
            self.setIcon(QtGui.QIcon(pixmap))

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QtCore.QSize(28, 28))

        self.setFixedWidth(90)
        self.setCheckable(True)
        self.setToolTip(theme.name.capitalize())
        self.setText(theme.name.capitalize())
