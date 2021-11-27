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

from .row import GroupWidget


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

                url = image.get('icon', None)
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


class GroupListItem(QtWidgets.QListWidgetItem):

    def __init__(self, device=None):
        super(GroupListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(200, 20))
        self.setSizeHint(QtCore.QSize(100, 65))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, device)


class GroupListWidget(QtWidgets.QListWidget):
    actionClick = QtCore.pyqtSignal(object)

    def __init__(self):
        super(GroupListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalScrollBar().setVisible(False)
        self.verticalScrollBar().setVisible(False)

        self.loaderImage = ImageThread()
        self.loaderImage.imageLoaded.connect(self.onImageLoaded)

    def onImageLoaded(self, event):
        data, callback = event
        if not callback: return None
        if not data: return None

        if not callable(callback):
            return None

        callback(data)

    def addGroup(self, entity):
        self.addEntity(entity)

    def addEntity(self, entity):
        item = GroupListItem(entity)
        self.addItem(item)

        widget = GroupWidget(entity)
        widget.actionClick.connect(self.actionClick.emit)
        self.setItemWidget(item, widget)

        icon = entity.get('icon', None)
        if not len(icon): return None

        self.loaderImage.append((entity, widget.onImageLoaded))
        if not self.loaderImage.isRunning():
            self.loaderImage.start()

    def clean(self, entity=None):
        self.loaderImage.clear()

        if not self.model(): return None

        count = self.model().rowCount()
        if not count: return None

        self.model().removeRows(0, count)

    def close(self):
        self.loaderImage.terminate()
        super().deleteLater()
        return super().close()
