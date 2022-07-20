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

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class DescriptionWidget(QtWidgets.QLabel):
    content = []

    def __init__(self, parent):
        super(DescriptionWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setWordWrap(True)

    def clear(self):
        self.setText('')

    def close(self):
        super().deleteLater()
        return super().close()


class CommentWidget(QtWidgets.QLabel):
    def __init__(self, text=None):
        super(CommentWidget, self).__init__()
        self.setWordWrap(True)
        self.setText(text)

    def close(self):
        super().deleteLater()
        return super().close()


class PreviewCommentsWidget(QtWidgets.QWidget):

    def __init__(self):
        super(PreviewCommentsWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.description = DescriptionWidget('...')
        self.layout().addWidget(self.description)
        self.layout().addWidget(CommentWidget('Comment line 1'))
        self.layout().addWidget(CommentWidget('Comment line 2'))
        self.layout().addWidget(CommentWidget('Comment line 3'))

    def setEntity(self, entity):
        self.description.setText(entity.get('description', None))

    def close(self):
        super().deleteLater()
        return super().close()
