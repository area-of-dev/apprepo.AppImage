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

from .row import PackageWidget


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

    def addEntity(self, entity=None):
        item = PackageListItem(entity)
        self.addItem(item)

        widget = PackageWidget(entity)
        self.setItemWidget(item, widget)

        return self

    def itemClickedEvent(self, item):
        return self.actionClick.emit(item.data(0))

    def clean(self, entity=None):
        if not self.model():
            return None
        self.model().removeRows(0, self.model().rowCount())
