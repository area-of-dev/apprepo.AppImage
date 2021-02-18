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


class ImageThread(QtCore.QThread):
    imageLoadedAction = QtCore.pyqtSignal(object)

    def __init__(self, entity):
        super(ImageThread, self).__init__()
        self.path = entity.url \
            if entity else None

    def run(self):
        if not self.path:
            return None

        url = self.path.replace('http://', 'https://')

        data = request.urlopen(url).read()
        self.imageLoadedAction.emit(data)

    # def __del__(self):
    #     self.wait()


class ImageWidget(QtWidgets.QLabel):
    def __init__(self, entity=None, width=400):
        super(ImageWidget, self).__init__()

        pixmap = QtGui.QPixmap('img/spinner.webp')
        self.setPixmap(pixmap.scaledToWidth(width))

        if not entity:
            return

        self.thread = ImageThread(entity)
        self.thread.imageLoadedAction.connect(self.onImageLoaded)
        self.thread.start()

    def onImageLoaded(self, data, width=400):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        self.setPixmap(pixmap.scaledToWidth(width))
        self.thread.terminate()
