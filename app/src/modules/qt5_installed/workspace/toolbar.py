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

from .button import PictureButtonFlat


class AppImageInstalledToolbarWidget(QtWidgets.QFrame):
    remove = QtCore.pyqtSignal(object)
    validate = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(AppImageInstalledToolbarWidget, self).__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        button = PictureButtonFlat('icons/remove')
        button.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        button.clicked.connect(lambda x: self.remove.emit(entity.path))
        button.setToolTipDuration(0)
        self.layout().addWidget(button)

        self.layout().addWidget(QtWidgets.QLabel('...'))

        button = PictureButtonFlat('icons/update')
        button.setToolTip('Download into the "~/Applications" folder and apply the system integration')
        button.clicked.connect(lambda x: self.update.emit(entity.path))
        button.setToolTipDuration(0)
        self.layout().addWidget(button)

    def setEntity(self, entity):
        self.entity = entity

    def close(self):
        super().deleteLater()
        return super().close()
