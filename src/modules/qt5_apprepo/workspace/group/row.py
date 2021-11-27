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

from modules.qt5_apprepo.workspace.group.image import ImageWidget


class Title(QtWidgets.QLabel):
    def __init__(self, title=None):
        super(Title, self).__init__(title)


class Description(QtWidgets.QLabel):
    def __init__(self, title=None):
        super(Description, self).__init__(title)
        self.setWordWrap(True)


class GroupWidget(QtWidgets.QWidget):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(GroupWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.entity = entity

        self.setToolTip(entity.get('name', None))
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.image = ImageWidget(entity.get('image', None))
        self.layout().addWidget(self.image, 0, 0, 2, 1)

        test = Title(entity.get('name', None))
        test.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(test, 0, 1, 1, 1)

        description = Description(entity.get('description', None))
        description.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(description, 1, 1, 1, 1)

    def onImageLoaded(self, data=None):
        if not self.image: return None
        if not data: return None

        try:
            self.image.onImageLoaded(data)
        except RuntimeError as ex:
            print(ex)
            pass

    def event(self, a0: QtCore.QEvent) -> bool:
        if a0.__class__.__name__ == "QMouseEvent":
            if a0.type() == QtCore.QEvent.MouseButtonRelease:
                self.actionClick.emit(self.entity)

        return super(GroupWidget, self).event(a0)
