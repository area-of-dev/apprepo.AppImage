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
import os

import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .image import ImageWidget
from .label import Title, Description


class ActionsItemListWidget(QtWidgets.QWidget):
    removeAction = QtCore.pyqtSignal(object)
    startAction = QtCore.pyqtSignal(object)
    infoAction = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(ActionsItemListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.image = ImageWidget(entity)
        self.layout().addWidget(self.image, 0, 0, 5, 1)

        if entity.package is not None:
            widget = Title(entity.package.get('name'))
            widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.layout().addWidget(widget, 0, 1, 1, 1)

            widget = Description(entity.package.get('version'))
            self.layout().addWidget(widget, 1, 1, 1, 1)

            widget = Description(entity.package.get('package'))
            self.layout().addWidget(widget, 2, 1, 1, 1)

            widget = Description(entity.package.get('description'))
            self.layout().addWidget(widget, 3, 1, 1, 1)

            widget = Description(entity.package.get('file'))
            self.layout().addWidget(widget, 4, 1, 1, 1)
            return None

        widget = Title(os.path.basename(entity.appimage))
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(widget, 0, 1, 1, 1)

        widget = Description(os.path.dirname(entity.appimage))
        self.layout().addWidget(widget, 1, 1, 1, 1)

        widget = Description(entity.appimage)
        self.layout().addWidget(widget, 2, 1, 1, 1)
