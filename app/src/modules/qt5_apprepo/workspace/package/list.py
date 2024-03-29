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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .list_item import PackageListItem
from .list_thread import PackageImageThread
from .list_widget import PackageWidget


class PackageListWidget(QtWidgets.QListWidget):
    actionClick = QtCore.pyqtSignal(object)
    actionInstall = QtCore.pyqtSignal(object)
    actionDownload = QtCore.pyqtSignal(object)
    actionRemove = QtCore.pyqtSignal(object)
    actionTest = QtCore.pyqtSignal(object)
    actionStart = QtCore.pyqtSignal(object)

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

        self.loaderImage = PackageImageThread()
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
        widget.actionInstall.connect(self.actionInstall.emit)
        widget.actionDownload.connect(self.actionDownload.emit)
        widget.actionRemove.connect(self.actionRemove.emit)
        widget.actionTest.connect(self.actionTest.emit)
        widget.actionStart.connect(self.actionStart.emit)

        self.setItemWidget(item, widget)

        preview = entity.get('preview', None)
        if not preview: return None

        self.loaderImage.append(
            (preview, widget.onImageLoaded)
        )

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
