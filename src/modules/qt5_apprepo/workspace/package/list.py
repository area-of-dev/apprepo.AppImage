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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .row import PackageWidget


class ImageThread(QtCore.QThread):
    imageLoaded = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ImageThread, self).__init__()
        self.stop = False
        self.images = []

    def append(self, image):
        self.images.append(image)
        return self

    def clear(self):
        self.images = []
        return self

    def run(self):

        while True:
            for (image, callback) in self.images:
                if not len(self.images): break

                url = image.get('url', None)
                if not url: continue

                data = request.urlopen(url).read()
                self.imageLoaded.emit((data, callback))

            if self.stop: break
            QtCore.QThread.msleep(300)

    def terminate(self) -> None:
        self.stop = True
        super().terminate()

    def __del__(self):
        self.wait()


class PackageListItem(QtWidgets.QListWidgetItem):

    def __init__(self, entity=None):
        super(PackageListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(400, 300))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, entity)


class PackageListWidget(QtWidgets.QListWidget):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self):
        super(PackageListWidget, self).__init__()
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QtWidgets.QListView.Static)

        self.setMinimumWidth(400)

        self.itemClicked.connect(self.itemClickedEvent)
        self.hashmap_index = {}

        self.loaderImage = ImageThread()
        self.loaderImage.imageLoaded.connect(self.onImageLoaded)

    def onImageLoaded(self, event):
        data, callback = event
        if not callback: return None
        if not data: return None

        if not callable(callback):
            return None

        callback(data)

    def addEntity(self, entity=None):
        item = PackageListItem(entity)
        self.addItem(item)

        widget = PackageWidget(entity)
        self.setItemWidget(item, widget)

        for image in entity.get('images', None):
            self.loaderImage.append((image, widget.onImageLoaded))
            break

        if not self.loaderImage.isRunning():
            self.loaderImage.start()

        return self

    def itemClickedEvent(self, item):
        return self.actionClick.emit(item.data(0))

    def clean(self, entity=None):
        self.loaderImage.clear()

        if not self.model(): return None

        count = self.model().rowCount()
        if not count: return None

        self.model().removeRows(0, count)

    def close(self):
        self.loaderImage.terminate()
        super(PackageListWidget, self).deleteLater()
        return super(PackageListWidget, self).close()
