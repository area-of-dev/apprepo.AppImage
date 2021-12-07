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


class DashboardWidget(QtWidgets.QWidget):

    @hexdi.inject('actions')
    def __init__(self, actions):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.list = ActionsListWidget()
        self.layout().addWidget(self.list)

        for entity in actions.actions():
            widget = ActionsItemListWidget(entity)
            self.list.addWidget(widget)
