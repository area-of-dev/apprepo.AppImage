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
import math
import os
import time
from collections import namedtuple
from datetime import datetime

import hexdi
from PyQt5 import QtCore

from modules.qt5_actions.storage.interface import ActionsStorage
from plugins import cmd_install, cmd_uninstall, cli_download, cli_integrate

Options = namedtuple('Options', 'force systemwide')


class BackgroundThread(QtCore.QThread):

    def __init__(self):
        super(BackgroundThread, self).__init__()

    @hexdi.inject('actions')
    def run(self, storage):
        while True:
            action = storage.next()
            if action is None:
                time.sleep(1)
                continue

            if action.action == 'integrate':
                appimage = action.appimage
                if not appimage: continue

                for output in cli_integrate.actions.integrate(appimage, Options(True, False)):
                    self._progress(100, 100, action)

            if action.action == 'download':
                package = action.package
                if not package: continue

                callback = functools.partial(self._progress, entity=action)
                for output in cli_download.actions.download(action.package, Options(True, False), callback):
                    print(output)

            if action.action == 'install':
                package = action.package
                if not package: continue

                callback = functools.partial(self._progress, entity=action)
                for output in cmd_install.actions.install(action.package, Options(True, False), callback):
                    print(output)

            if action.action == 'remove':
                appimage = action.appimage
                if not appimage: continue

                appimage = os.path.basename(appimage)
                if not appimage: continue

                for output in cmd_uninstall.actions.remove(appimage, None):
                    self._progress(100, 100, action)

    def _progress(self, x, y, entity=None):

        entity.progress = math.ceil(x / y * 100)
        if entity.progress < 100: return
        entity.finished_at = datetime.now()

    @hexdi.inject('actions')
    def start(self, actions: ActionsStorage) -> None:
        super().start()

    def terminate(self) -> None:
        super().terminate()
