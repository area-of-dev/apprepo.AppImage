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

from .theme.manager import ServiceTheme


@hexdi.permanent('themes')
class ServiceThemeInstance(ServiceTheme):
    @hexdi.inject('config')
    def __init__(self, config):
        themes_default = 'themes/'
        themes_custom = '~/.config/PerformanceTuner/themes'

        super(ServiceThemeInstance, self).__init__([
            config.get('themes.default', themes_default),
            config.get('themes.custom', themes_custom)
        ])
