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

from .image import ImageWidget
from .label import Title, Description
from .preview.toolbar import PreviewToolbarWidget


class PackageWidget(QtWidgets.QGroupBox):
    actionClick = QtCore.pyqtSignal(object)
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

    def __init__(self, entity):
        super(PackageWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(entity.get('name', None))
        self.layout.addWidget(title, 0, 0, 1, 2)

        self.image = ImageWidget(entity.get('image', None))
        self.layout.addWidget(self.image, 1, 0, 2, 2)

        description = Description(entity.get('description', None))
        description.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        description.setWordWrap(True)
        self.layout.addWidget(description, 2, 0, 1, 2)

        self.toolbar = PreviewToolbarWidget(entity)
        self.toolbar.actionInstall.connect(self.actionInstall.emit)
        self.toolbar.actionDownload.connect(self.actionDownload.emit)
        self.toolbar.actionRemove.connect(self.actionRemove.emit)
        self.toolbar.actionTest.connect(self.actionTest.emit)
        self.toolbar.actionStart.connect(self.actionStart.emit)

        self.layout.addWidget(self.toolbar, 0, 2, 3, 1)

        self.setLayout(self.layout)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)
        self.setGraphicsEffect(effect)

    def onImageLoaded(self, data=None):
        if not self.image: return None
        if not data: return None

        try:
            self.image.onImageLoaded(data)
        except RuntimeError as ex:
            print(ex)
            pass

    def event(self, QEvent):
        if QEvent.__class__.__name__ == "QMouseEvent":
            if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
                self.actionClick.emit(QEvent)

        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(10)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        return super(PackageWidget, self).event(QEvent)

    def close(self):
        super(PackageWidget, self).deleteLater()
        return super(PackageWidget, self).close()
