# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
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

from .actions import ModuleActions
from .workspace.content import WindowContent
from .workspace.header import ToolbarWidget
from .workspace.window import MainWindow


@hexdi.permanent('window.content')
class WindowContentInstance(WindowContent):
    pass


@hexdi.permanent('window.header')
class WindowContentInstance(ToolbarWidget):
    pass


@hexdi.permanent('window.actions')
class ModuleActionsInstance(ModuleActions):
    pass


@hexdi.permanent('window')
class MainWindowInstance(MainWindow):
    @hexdi.inject('config', 'window.header', 'window.content', 'window.actions')
    def __init__(self, config, header, content, actions):
        super(MainWindowInstance, self).__init__()

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setContentsMargins(0, 0, 0, 0)
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        self.centralWidget().layout().addWidget(header)
        self.centralWidget().layout().addWidget(content)

        self.resizeAction.connect(actions.resizeActionEvent)

        width = int(config.get('window.width', 400))
        height = int(config.get('window.height', 500))
        self.resize(width, height)
