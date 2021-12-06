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
import math
from urllib import request

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .dashboard_thread import ImageThread
from .image import ImageWidget


class PreviewPicturesWidget(QtWidgets.QWidget):

    def __init__(self, entity=None):
        super(PreviewPicturesWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.preview = ImageWidget(None, self.width() / 1.5)
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

    def onImageSelected(self, entity):

        url = entity.get('url', None)
        if not url: return None

        data = request.urlopen(url).read()
        if not data: return None

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        pixmap = pixmap.scaledToWidth(self.width() / 1.3)
        if not pixmap: return None

        self.preview.setPixmap(pixmap)

    def setEntity(self, entity):
        self.entity = entity
        self.clear()

        images = entity.get('images', [])
        if not len(images): return None

        row = 1
        for col, image in enumerate(images, start=0):
            widget = ImageWidget(image, 200)
            widget.actionClick.connect(self.onImageSelected)
            self.layout().addWidget(widget, row, (col % 3))
            row = row if (col % 3) < 2 else row + 1

            if not callable(widget.onImageLoaded): continue
            self.thread.append((image, widget.onImageLoaded))

        for image in images:
            self.preview = ImageWidget(image, self.width() / 1.3)
            self.layout().addWidget(self.preview, 0, 0, 1, 3)

            if not callable(self.preview.onImageLoaded): break
            self.thread.append((image, self.preview.onImageLoaded))
            break

        self.thread.start()

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
