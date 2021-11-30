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

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ImageWidget(QtWidgets.QLabel):

    def __init__(self, entity=None, width=70):
        super(ImageWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)

        pixmap = QtGui.QPixmap(entity)
        pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
        if not pixmap: return None

        self.setPixmap(pixmap)

    def close(self):
        super().deleteLater()
        return super().close()
