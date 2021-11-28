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
    imageLoaded = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ImageThread, self).__init__()
        self.stop = False
        self.is_pending = True
        self.images = []

    def append(self, image):
        self.images.append(image)
        return self

    def clear(self):
        self.is_pending = True
        self.images = []
        return self

    def run(self):

        while not self.stop:
            if self.is_pending:
                for (image, callback) in self.images:
                    if not len(self.images): break

                    url = image.get('url', None)
                    if not url: continue

                    data = request.urlopen(url).read()
                    self.imageLoaded.emit((data, callback))
                self.is_pending = False

            QtCore.QThread.msleep(300)

    def terminate(self) -> None:
        self.stop = True
        super().terminate()

    def __del__(self):
        self.wait()


class PictureWidget(QtWidgets.QLabel):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self, entity=None, width=200):
        super(PictureWidget, self).__init__()
        self.entity = entity
        self.width = width

        pixmap = QtGui.QPixmap('img/spinner.webp')
        pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)

        if not pixmap: return None
        self.setPixmap(pixmap)

    def onImageLoaded(self, data=None):
        if not data: return None

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaledToWidth(self.width, Qt.SmoothTransformation)

        if not pixmap: return None
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev):
        self.actionClick.emit(self.entity)

    def close(self):
        super().deleteLater()
        return super().close()


class PreviewPicturesWidget(QtWidgets.QWidget):

    def __init__(self, entity=None):
        super(PreviewPicturesWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.preview = PictureWidget(None, 200 * 3)
        self.layout().addWidget(self.preview, 0, 0, 1, 3)

        self.thread = ImageThread()
        self.thread.imageLoaded.connect(self.onImageLoaded)

    def onImageLoaded(self, event):
        data, callback = event
        if not callback: return None
        if not data: return None

        try:
            if callable(callback):
                callback(data)
        except RuntimeError as ex:
            print(ex)

    def setEntity(self, entity):
        self.entity = entity
        self.clear()

        for index, image in enumerate(entity.get('images', None), start=0):
            self.preview = PictureWidget(image, 200 * 3)
            self.layout().addWidget(self.preview, 0, 0, 1, 3)

            if not callable(self.preview.onImageLoaded): break
            self.thread.append((image, self.preview.onImageLoaded))
            break

        for index, image in enumerate(entity.get('images', None), start=0):
            widget = PictureWidget(image)
            widget.actionClick.connect(self.onImageSelected)
            self.layout().addWidget(widget, 1, index)

            if not callable(widget.onImageLoaded): continue
            self.thread.append((image, widget.onImageLoaded))

        self.thread.start()

    def onImageSelected(self, entity):

        url = entity.get('url', None)
        if not url: return None

        data = request.urlopen(url).read()
        if not data: return None

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        pixmap = pixmap.scaledToWidth(self.preview.width)
        if not pixmap: return None

        self.preview.setPixmap(pixmap)

    def clear(self):
        self.thread.clear()

        while self.layout().count():
            child = self.layout().takeAt(0)
            if not child: continue

            if not child.widget(): continue
            child.widget().deleteLater()

    def close(self):
        self.thread.terminate()

        super(PreviewPicturesWidget, self).deleteLater()
        return super(PreviewPicturesWidget, self).close()
