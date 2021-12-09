# Copyright 2021 Alex Woroschilow (alex.woroschilow@gmail.com)
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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from modules.qt5_actions.workspace.list import ActionsListWidget
from modules.qt5_actions.workspace.list_widget import ActionsItemListWidget
from modules.qt5_actions.workspace.thread import WorkspaceThread


class DashboardWidget(QtWidgets.QWidget):

    def __init__(self):
        super(DashboardWidget, self).__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.list = ActionsListWidget()
        self.layout().addWidget(self.list)

        self.thread_updater = WorkspaceThread()
        self.thread_updater.progress.connect(self.progress)
        self.thread_updater.start()

        self.update(None)

    def progress(self, bunch):
        (entity, callback) = bunch
        if not callable(callback): return None
        callback(entity)

    @hexdi.inject('actions')
    def update(self, entity=None, actions=None):
        self.list.clean()
        for entity in actions.actions():
            widget = ActionsItemListWidget(entity)
            self.list.addWidget(widget)

            self.thread_updater.append((entity, widget.update))
