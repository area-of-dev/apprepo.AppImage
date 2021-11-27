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


class ImageThread(QtCore.QThread):
    imageLoadedAction = QtCore.pyqtSignal(object)

    def __init__(self, entity):
        super(ImageThread, self).__init__()
        self.path = entity.get('url', None) \
            if entity else None

    def run(self):
        if not self.path:
            return None

        url = self.path.replace('http://', 'https://')

        data = request.urlopen(url).read()
        self.imageLoadedAction.emit(data)

    def __del__(self):
        self.wait()


class PictureWidget(QtWidgets.QLabel):
    def __init__(self, entity=None, width=200):
        super(PictureWidget, self).__init__()
        self.width = width

        pixmap = QtGui.QPixmap('img/spinner.webp')
        self.setPixmap(pixmap.scaledToWidth(width))

        if not entity:
            return

        self.thread = ImageThread(entity)
        self.thread.imageLoadedAction.connect(self.onImageLoaded)
        self.thread.start()

    def onImageLoaded(self, data):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        self.setPixmap(pixmap.scaledToWidth(self.width))
        self.thread.terminate()


class PreviewPicturesWidget(QtWidgets.QWidget):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(PreviewPicturesWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.layout().addWidget(PictureWidget(None, 200 * 3), 0, 0, 1, 3)
        self.layout().addWidget(PictureWidget(), 1, 0)
        self.layout().addWidget(PictureWidget(), 1, 1)
        self.layout().addWidget(PictureWidget(), 1, 2)

    def setEntity(self, entity):
        self.entity = entity
        self.clear()

        for image in entity.get('images', None):
            self.layout().addWidget(PictureWidget(image, 200 * 3), 0, 0, 1, 3)
            break

        for index, image in enumerate(entity.get('images', None), start=0):
            self.layout().addWidget(PictureWidget(image), 1, index)

    def clear(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
