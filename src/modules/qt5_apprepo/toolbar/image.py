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

import pathlib

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ImageWidget(QtWidgets.QLabel):

    def __init__(self, entity=None, width=70):
        super(ImageWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)

        pixmap = QtGui.QPixmap(entity)
        pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
        if not pixmap: return None

        self.setPixmap(pixmap)

    def close(self):
        super().deleteLater()
        return super().close()


class DragAndDropImageWidget(QtWidgets.QLabel):
    drop = QtCore.pyqtSignal(object)

    def __init__(self, entity=None, width=70):
        super(DragAndDropImageWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
        self.setMaximumWidth(350)
        self.setAcceptDrops(True)

        pixmap = QtGui.QPixmap(entity)
        pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
        if not pixmap: return None

        self.setPixmap(pixmap)

    def dragEnterEvent(self, event):
        filename = event.mimeData().text()
        suffix = pathlib.Path(filename).suffix
        if suffix.replace('.', '') in ['AppImage']:
            return event.acceptProposedAction()
        return event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().text()
        self.drop.emit(file_path.replace('file://', ''))

    def event(self, QEvent):
        if QEvent.__class__.__name__ == "QEnterEvent":
            if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
                print(QEvent.__class__.__name__)
                self.drop.emit(QEvent)

        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(5)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        return super(DragAndDropImageWidget, self).event(QEvent)

    def close(self):
        super().deleteLater()
        return super().close()
