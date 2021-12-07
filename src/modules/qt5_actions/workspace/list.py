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

from .list_item import SettingsListItem


class ActionsListWidget(QtWidgets.QListWidget):
    # actionUpdate = QtCore.pyqtSignal(object)
    # actionRemove = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ActionsListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def addWidget(self, widget):
        item = SettingsListItem()
        self.addItem(item)

        self.setItemWidget(item, widget)

    def clean(self, entity=None):
        if not self.model(): return None

        count = self.model().rowCount()
        if not count: return None

        self.model().removeRows(0, count)
