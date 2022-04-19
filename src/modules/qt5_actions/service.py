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
from datetime import datetime

import hexdi

from .storage.interface import ActionsStorage
from .storage.schema import Action
from .thread.background import BackgroundThread
from .workspace.dashboard import DashboardWidget


@hexdi.permanent('workspace.actions')
class DashboardWidgetInstance(DashboardWidget):
    pass


@hexdi.permanent('thread.actions')
class WorkspaceThreadInstance(BackgroundThread):
    pass


@hexdi.permanent('actions')
class ActionsStorageInstance(ActionsStorage):

    def install(self, model):
        self.add_action({
            'action': 'install',
            'package': model,
        })

    def download(self, model):
        self.add_action({
            'action': 'download',
            'package': model,
        })

    def validate(self, model):
        self.add_action({
            'action': 'validate',
            'package': model,
        })

    def remove(self, model):
        self.add_action({
            'action': 'remove',
            'appimage': model,
        })

    def integrate(self, model):
        self.add_action({
            'action': 'integrate',
            'appimage': model,
        })

    def start(self, model):
        self.add_action({
            'action': 'start',
            'appimage': model,
        })

    def stop(self, model):
        model.cancelled_at = datetime.now()
        self.session.flush()
        return model

    def restart(self, model):
        model.progress = 0
        model.cancelled_at = None
        model.finished_at = None
        self.session.flush()
        return model

    def clean(self, model: Action):
        model.finished_at = datetime.now()
        self.session.flush()
        return model
