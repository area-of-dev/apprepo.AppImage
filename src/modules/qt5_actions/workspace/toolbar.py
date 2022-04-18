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
from ..storage.schema import Action


class ActionsToolbarWidget(QtWidgets.QFrame):
    remove = QtCore.pyqtSignal(object)
    stop = QtCore.pyqtSignal(object)
    restart = QtCore.pyqtSignal(object)

    def __init__(self, entity: Action = None):
        super(ActionsToolbarWidget, self).__init__()

        self.entity = entity

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.buttonRemove = PictureButtonFlat('icons/remove')
        self.buttonRemove.setToolTip('Remove this action from the list')
        self.buttonRemove.clicked.connect(lambda x: self.remove.emit(self.entity))
        self.layout().addWidget(self.buttonRemove)

        self.buttonStop = PictureButtonFlat('icons/stop')
        self.buttonStop.setToolTip('Stop current activity')
        self.buttonStop.setDisabled(entity.cancelled_at is not None)
        self.buttonStop.clicked.connect(lambda x: self.stop.emit(self.entity))
        self.layout().addWidget(self.buttonStop)

        self.buttonRestart = PictureButtonFlat('icons/restart')
        self.buttonRestart.setToolTip('Restart cancelled process')
        self.buttonRestart.setDisabled(entity.cancelled_at is None)
        self.buttonRestart.clicked.connect(lambda x: self.restart.emit(self.entity))
        self.layout().addWidget(self.buttonRestart)

    def close(self):
        super().deleteLater()
        return super().close()
