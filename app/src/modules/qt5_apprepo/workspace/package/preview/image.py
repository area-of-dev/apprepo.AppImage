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

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsBlurEffect


class ImageWidget(QtWidgets.QLabel):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, entity=None, width=200):
        super(ImageWidget, self).__init__()
        self.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.entity = entity
        self.width = width

        pixmap = QtGui.QPixmap('icons/spinner')
        self.setPixmap(pixmap.scaledToWidth(width))

    def onImageLoaded(self, data):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        pixmap = pixmap.scaledToWidth(self.width, Qt.SmoothTransformation)
        if not pixmap: return None

        self.setPixmap(pixmap)

        # creating a blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(1)
        self.setGraphicsEffect(blur_effect)

    def mousePressEvent(self, ev):
        self.actionClick.emit(self.entity)

    def close(self):
        super().deleteLater()
        return super().close()
