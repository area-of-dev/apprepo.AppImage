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
from modules.qt5_actions.storage.schema import Action
from plugins import cli_download
from plugins import cli_install
from plugins import cli_integrate
from plugins import cli_validate
from plugins import cmd_uninstall

Options = namedtuple('Options', 'force systemwide')


class BackgroundThread(QtCore.QThread):

    def __init__(self):
        super(BackgroundThread, self).__init__()
        self.storage = ActionsStorage()

    def _do_integrate(self, action):
        appimage = action.appimage
        if not appimage: return
        for output in cli_integrate.actions.integrate(appimage, Options(True, False)):
            yield self._progress(100, 100, action)

    def _do_download(self, action):
        package = action.package
        if not package: return

        print("!!!", package)
        callback = functools.partial(self._progress, entity=action)
        for output in cli_download.actions.download(action.package, Options(True, False), callback):
            yield output

    def _do_install(self, action):
        package = action.package
        if not package: return
        callback = functools.partial(self._progress, entity=action)
        for output in cli_install.actions.install(action.package, Options(True, False), callback):
            yield output

    def _do_remove(self, action):
        appimage = action.appimage
        if not appimage: return
        appimage = os.path.basename(appimage)
        if not appimage: return
        for output in cmd_uninstall.actions.remove(appimage, None):
            yield self._progress(100, 100, action)

    def _do_validate(self, action):
        package = action.package
        if not package: return
        callback = functools.partial(self._progress, entity=action)
        for output in cli_validate.actions.validate(action.package, Options(True, False), callback):
            yield output

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

    def run(self):

        mapping: dict = {
            "integrate": self._do_integrate,
            "download": self._do_download,
            "install": self._do_install,
            "remove": self._do_remove,
            "validate": self._do_validate,
        }

        while True:
            action: Action = self.storage.next()
            if action is None:
                time.sleep(1)
                continue

            try:
                if action.action not in mapping:
                    continue

                callback = mapping[action.action]
                if not callable(callback):
                    continue

                for output in callback(action):
                    print(output)

            except Exception:
                pass

    @hexdi.inject('actions')
    def start(self, actions: ActionsStorage) -> None:
        super().start()

    def terminate(self) -> None:
        super().terminate()
