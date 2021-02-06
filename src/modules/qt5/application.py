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
import sys

import hexdi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Application(QtWidgets.QApplication):

    def __init__(self, options: {} = None, args: [] = None):
        super(Application, self).__init__(sys.argv)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.setApplicationName('Apprepo - Desktop client')

        from modules.kernel import kernel
        self.kernel = kernel.Kernel(options, args)

    @hexdi.inject('window')
    def exec_(self, options: {}, args: [], window: QtWidgets.QMainWindow):
        if window is None: return None

        self.setActiveWindow(window)
        window.exit.connect(self.exit)
        window.show()

        return super(Application, self).exec_()
