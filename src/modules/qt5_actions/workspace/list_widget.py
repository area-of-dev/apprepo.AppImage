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
import os

import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .image import ImageWidget
from .label import Title, Description
from .toolbar import ActionsToolbarWidget


class ActionsItemListWidget(QtWidgets.QWidget):
    removeAction = QtCore.pyqtSignal(object)
    restartAction = QtCore.pyqtSignal(object)
    stopAction = QtCore.pyqtSignal(object)

    def __init__(self, entity=None):
        super(ActionsItemListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        if entity.package is not None:
            return self.__init__remote__(entity)
        return self.__init__local__(entity)

    def __init__remote__(self, entity=None):
        self.image = ImageWidget(entity)
        self.layout().addWidget(self.image, 0, 0, 5, 1)

        widget = Title("{}: {}".format(entity.action.capitalize(), entity.package.get('name')))
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(widget, 0, 1, 1, 1)

        widget = Description(entity.package.get('version'))
        self.layout().addWidget(widget, 1, 1, 1, 1)

        widget = Description(entity.package.get('package'))
        self.layout().addWidget(widget, 2, 1, 1, 1)

        widget = Description(entity.package.get('description'))
        self.layout().addWidget(widget, 3, 1, 1, 1)

        widget = Description(entity.package.get('file'))
        self.layout().addWidget(widget, 4, 1, 1, 1)

        widget = Description(entity.package.get('file'))
        self.layout().addWidget(widget, 4, 1, 1, 1)

        self.toolbar = ActionsToolbarWidget(entity)
        self.toolbar.remove.connect(self.removeAction.emit)
        self.toolbar.restart.connect(self.restartAction.emit)
        self.toolbar.stop.connect(self.stopAction.emit)
        self.layout().addWidget(self.toolbar, 3, 0, 2, 1)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout().addWidget(self.progress, 5, 1, 1, 1)

    def __init__local__(self, entity=None):
        self.image = ImageWidget(entity)
        self.layout().addWidget(self.image, 0, 0, 5, 1)

        widget = Title("{}: {}".format(entity.action.capitalize(), os.path.basename(entity.appimage)))
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(widget, 0, 1, 1, 1)

        widget = Description(os.path.dirname(entity.appimage))
        self.layout().addWidget(widget, 1, 1, 1, 1)

        widget = Description(entity.appimage)
        self.layout().addWidget(widget, 2, 1, 1, 1)

        self.toolbar = ActionsToolbarWidget(entity)
        self.toolbar.remove.connect(self.removeAction.emit)
        self.toolbar.restart.connect(self.restartAction.emit)
        self.toolbar.stop.connect(self.stopAction.emit)
        self.layout().addWidget(self.toolbar, 3, 0, 2, 1)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout().addWidget(self.progress, 3, 1, 1, 1)

    @hexdi.inject('actions')
    def update(self, entity, storage):
        if not hasattr(entity, 'progress'):
            return self

        if hasattr(storage, 'session'):
            storage.session.refresh(entity)

        if entity.progress >= 100:
            self.progress.setValue(100)
            self.progress.setVisible(False)
            self.destroy()
            return self

        self.progress.setValue(entity.progress)
        self.progress.setVisible(True)
        return self
