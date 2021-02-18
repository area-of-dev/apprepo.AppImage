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

from .row import GroupWidget


class GroupListItem(QtWidgets.QListWidgetItem):

    def __init__(self, device=None):
        super(GroupListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(200, 20))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, device)


class GroupListWidget(QtWidgets.QListWidget):
    actionClick = QtCore.pyqtSignal(object)

    @hexdi.inject('apprepo.cache')
    def __init__(self, cache):
        super(GroupListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def addGroup(self, entity):
        self.addEntity(entity)

    def addEntity(self, entity):
        item = GroupListItem(entity)
        self.addItem(item)

        widget = GroupWidget(entity)
        widget.actionClick.connect(self.actionClick.emit)
        self.setItemWidget(item, widget)

    def clean(self, entity=None):
        if not self.model():
            return None
        self.model().removeRows(0, self.model().rowCount())
