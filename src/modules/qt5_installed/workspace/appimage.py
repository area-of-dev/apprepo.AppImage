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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .image import ImageWidget
from .label import Title, Description


class AppImageInstalledWidget(QtWidgets.QWidget):
    actionUpdate = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, appimage=None, config=None):
        super(AppImageInstalledWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setToolTip(appimage.path)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.image = ImageWidget(appimage.icon)
        self.layout().addWidget(self.image, 0, 0, 5, 1)

        title = Title(appimage.name)
        title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(title, 0, 1, 1, 1)

        description = Description(appimage.alias)
        self.layout().addWidget(description, 1, 1, 1, 1)

        description = Description(appimage.path)
        self.layout().addWidget(description, 2, 1, 1, 1)

        description = Description(appimage.icon)
        self.layout().addWidget(description, 3, 1, 1, 1)

        description = Description(appimage.desktop)
        self.layout().addWidget(description, 4, 1, 1, 1)

        # self.start = ToolbarButton(self, "Run", QtGui.QIcon('icons/start'))
        # self.start.clicked.connect(self.actionStart.emit)
        # self.start.setToolTip("Start: {}".format(appimage.path))
        # self.layout().addWidget(self.start, 0, 2, 2, 1)
        #
        # if appimage.outdated and appimage.slug:
        #     self.update = ToolbarButton(self, "Update", QtGui.QIcon('icons/update'))
        #     self.update.clicked.connect(self.actionUpdate.emit)
        #     self.update.setToolTip("Update: {}".format(appimage.path))
        #     self.layout().addWidget(self.update, 0, 3, 2, 1)
        #
        # self.remove = ToolbarButton(self, "Remove", QtGui.QIcon('icons/remove'))
        # self.remove.clicked.connect(self.actionRemove.emit)
        # self.remove.setToolTip("Remove: {}".format(appimage.path))
        # self.layout().addWidget(self.remove, 0, 4, 2, 1)
