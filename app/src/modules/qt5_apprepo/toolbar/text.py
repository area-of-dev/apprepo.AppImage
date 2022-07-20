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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class SearchField(QtWidgets.QLineEdit):
    search = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(SearchField, self).__init__(parent)
        self.setPlaceholderText('Enter the search string...')
        self.setFocusPolicy(Qt.StrongFocus)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self)
        shortcut.activated.connect(self.on_shortcut_activated)

        self.returnPressed.connect(lambda: self.search.emit(self.text()))

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

    def on_shortcut_activated(self, event=None):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(10)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(5)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)

        return super(SearchField, self).event(QEvent)
