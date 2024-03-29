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
from modules.qt5 import window

from .toolbar.panel import ToolbarWidget


@window.toolbar(name='Themes', focus=False, position=6)
def window_toolbar(parent=None):
    widget = ToolbarWidget()
    parent.actionReload.connect(widget.reload)
    return widget
