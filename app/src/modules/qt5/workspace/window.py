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
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    resizeAction = QtCore.pyqtSignal(object)
    exit = QtCore.pyqtSignal(object)

    @hexdi.inject('themes')
    def __init__(self, themes=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Apprepo - Desktop client')

        if os.path.exists('icons/hand.svg'):
            self.setWindowIcon(QtGui.QIcon("icons/hand"))

        self.setStyleSheet(themes.get_stylesheet())

    def resizeEvent(self, event):
        self.resizeAction.emit(event)
