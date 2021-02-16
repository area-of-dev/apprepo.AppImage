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
from urllib import request

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .label import Title


class PackageWidget(QtWidgets.QGroupBox):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, document):
        super(PackageWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.document = document

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(document.name)
        self.layout.addWidget(title, 0, 0, 1, 27)

        self.image = QtWidgets.QLabel()

        pixmap = QtGui.QPixmap()
        data = request.urlopen('https://pythonspot.com/wp-content/uploads/2016/07/pyqt5-qpixmap.png.webp').read()
        pixmap.loadFromData(data)
        self.image.setPixmap(pixmap.scaledToWidth(400))

        self.layout.addWidget(self.image, 1, 0, 4, 30)

        self.setLayout(self.layout)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)
        self.setGraphicsEffect(effect)

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
