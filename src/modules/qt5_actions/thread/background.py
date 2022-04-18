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
from plugins import cli_install, cmd_uninstall, cli_download, cli_integrate, cli_validate

Options = namedtuple('Options', 'force systemwide')


class BackgroundThread(QtCore.QThread):

    def __init__(self):
        super(BackgroundThread, self).__init__()
        self.storage = ActionsStorage()

    def run(self):
        while True:
            action = self.storage.next()
            if action is None:
                time.sleep(1)
                continue

            if action.action in ['integrate']:
                appimage = action.appimage
                if not appimage: continue

                try:
                    for output in cli_integrate.actions.integrate(appimage, Options(True, False)):
                        self._progress(100, 100, action)
                except Exception:
                    pass

            if action.action in ['download']:
                package = action.package
                if not package: continue
                try:
                    callback = functools.partial(self._progress, entity=action)
                    for output in cli_download.actions.download(action.package, Options(True, False), callback):
                        print(output)
                except Exception:
                    pass

            if action.action in ['install']:
                package = action.package
                if not package: continue

                try:
                    callback = functools.partial(self._progress, entity=action)
                    for output in cli_install.actions.install(action.package, Options(True, False), callback):
                        print(output)
                except Exception:
                    pass

            if action.action in ['remove']:
                appimage = action.appimage
                if not appimage: continue

                appimage = os.path.basename(appimage)
                if not appimage: continue

                try:
                    for output in cmd_uninstall.actions.remove(appimage, None):
                        self._progress(100, 100, action)
                except Exception:
                    pass

            if action.action in ['validate']:
                package = action.package
                if not package: continue

                try:
                    callback = functools.partial(self._progress, entity=action)
                    for output in cli_validate.actions.validate(action.package, Options(True, False), callback):
                        print(output)
                except Exception:
                    pass

    def _progress(self, x, y, entity=None):
        """

        :param x:
        :param y:
        :param entity:
        :param storage:
        :return:
        """

        self.storage.session.refresh(entity)
        entity.progress = math.ceil(x / y * 100)
        self.storage.session.flush()

        if entity.finished_at is not None or entity.cancelled_at is not None:
            raise Exception('Activity cancelled by user')

        if entity.progress < 100: return
        entity.finished_at = datetime.now()
        self.storage.session.flush()

    @hexdi.inject('actions')
    def start(self, actions: ActionsStorage) -> None:
        super().start()

    def terminate(self) -> None:
        super().terminate()
