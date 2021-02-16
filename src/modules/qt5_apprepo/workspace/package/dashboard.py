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

from .label import Title
from .list import PackageListWidget


class PackageDashboardWidget(QtWidgets.QWidget):
    selectAction = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PackageDashboardWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.title = Title('...')
        self.layout().addWidget(self.title)

        self.list = PackageListWidget()
        self.list.selectAction.connect(self.selectAction.emit)
        self.layout().addWidget(self.list)

    def setTitle(self, text):
        self.title.setText(text.capitalize())
        return self

    def setPreview(self, collection=[]):
        self.list.setPreview(collection)
        return self

    def addPreview(self, document=None):
        self.list.addPreview(document)
        return self

    def count(self):
        return self.list.count()
