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

import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .checkbox import CheckboxTriState


class SchemaWidget(QtWidgets.QLabel):
    def __init__(self, device=None):
        super(SchemaWidget, self).__init__('...')
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.setMinimumWidth(150)

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(functools.partial(
            self.refreshEvent, device=device
        ))
        self.timerRefresh.start(1000)

    def refreshEvent(self, device=None):
        self.setText('<b>{}</b>'.format(device.governor))


class FrequenceWidget(QtWidgets.QLabel):
    def __init__(self, device=None):
        super(FrequenceWidget, self).__init__('...')
        self.setAlignment(Qt.AlignVCenter)
        self.setMinimumWidth(100)

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(functools.partial(
            self.refreshEvent, device=device
        ))
        self.timerRefresh.start(1000)

    def refreshEvent(self, device=None):
        self.setText('{:>.1f} GHz'.format(
            device.frequence / 1000000
        ))


class DeviceWidget(QtWidgets.QWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, device=None, config=None):
        super(DeviceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.setToolTip(device.path)

        self.device = device

        default = config.get('cpu.permanent.{}'.format(self.device.code), 0)
        self.checkbox = CheckboxTriState(['Auto', 'Powersave', 'Performance'], int(default))
        self.checkbox.stateChanged.connect(self.deviceToggleEvent)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.layout().addWidget(self.checkbox, 0, 0)
        self.layout().addWidget(SchemaWidget(device), 0, 1)
        self.layout().addWidget(QtWidgets.QLabel(device.name.replace('Cpu', 'CPU ')), 0, 2)
        self.layout().addWidget(FrequenceWidget(device), 0, 3)

    @hexdi.inject('config')
    def deviceToggleEvent(self, value, config):
        config.set('cpu.permanent.{}'.format(self.device.code), int(value))
        self.toggleDeviceAction.emit((value, self.device))
