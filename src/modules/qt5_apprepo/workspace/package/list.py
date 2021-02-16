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
import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .row import PackageWidget


class PackageListItem(QtWidgets.QListWidgetItem):

    def __init__(self, entity=None):
        super(PackageListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(400, 500))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, entity)


class PackageListWidget(QtWidgets.QListWidget):
    selectAction = QtCore.pyqtSignal(object)

    @hexdi.inject('apprepo.cache')
    def __init__(self, apprepo=None):
        super(PackageListWidget, self).__init__()
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QtWidgets.QListView.Static)

        self.setMinimumWidth(400)

        self.itemClicked.connect(self.itemClickedEvent)

        for index, entity in enumerate(apprepo.packages(), start=0):
            self.addEntity(entity)
            if index > 10:
                break

        self.hashmap_index = {}

    def addEntity(self, entity=None):
        item = PackageListItem(entity)
        self.addItem(item)

        widget = PackageWidget(entity)
        self.setItemWidget(item, widget)

        return self

    def itemClickedEvent(self, item):
        document = item.data(0)
        return self.selectAction.emit(document)

    def count(self):
        return len(self.hashmap_index.keys())
