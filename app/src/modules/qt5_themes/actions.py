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

import hexdi


class ModuleActions(object):

    @hexdi.inject('config', 'window')
    def on_action_theme(self, config=None, window=None, theme=None, widget=None):
        if theme is None: return None
        if config is None: return None
        if window is None: return None
        if widget is None: return None

        config.set('themes.theme', theme.name)
        window.setStyleSheet(theme.stylesheet)
