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
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class CheckboxButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super(CheckboxButton, self).__init__(text)
        self.setFlat(True)
        self.value = None

    def setValue(self, value):
        self.value = value
        return self


class CheckboxTriState(QtWidgets.QWidget):
    stateChanged = QtCore.pyqtSignal(object)

    def __init__(self, values=[], default=0):
        super(CheckboxTriState, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.pool = []
        for index, name in enumerate(values, start=0):
            button = CheckboxButton(name)
            button.setCheckable(True)
            button.setValue(index)
            button.clicked.connect(functools.partial(
                self.toggle_state, widget=button
            ))

            self.layout().addWidget(button)
            self.pool.append(button)

        if default is None: return None

        if len(self.pool) > default:
            button = self.pool[default]
            button.setChecked(True)

    def toggle_state(self, state, widget=None):
        for index, button in enumerate(self.pool, start=0):
            button_state = False if button is not widget else state
            button.setChecked(button_state)

        for index, button in enumerate(self.pool, start=0):
            if not button.isChecked():
                continue
            return self.stateChanged.emit(index)

        button = self.pool[0]
        button.setChecked(True)
        return self.stateChanged.emit(0)
