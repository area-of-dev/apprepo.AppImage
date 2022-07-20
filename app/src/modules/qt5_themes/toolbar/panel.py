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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ToolbarButton


class ToolbarWidget(QtWidgets.QScrollArea):
    @hexdi.inject('themes')
    def __init__(self, themes=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidgetResizable(True)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QHBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        self.buttons = []

        for theme in themes.get_stylesheets():
            button = ToolbarButton(self, theme)
            button.actionClick.connect(self.toggleThemeEvent)
            self.addWidget(button)

            self.buttons.append(button)

        self.reload(None)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget)

    @hexdi.inject('config')
    def reload(self, event, config=None):
        for button in self.buttons:
            if not button.theme:
                continue

            button.setChecked(button.theme.name == config.get('themes.theme'))

    @hexdi.inject('config', 'window')
    def toggleThemeEvent(self, theme, config, window):
        if not theme: return None
        config.set('themes.theme', theme.name)
        window.setStyleSheet(theme.stylesheet)
        self.reload(None)
