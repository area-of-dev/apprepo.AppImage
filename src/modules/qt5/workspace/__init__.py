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
import hexdi


def workspace(*args, **kwargs):
    name = kwargs.get('name', 'New Tab')
    position = kwargs.get('position', 0)
    focus = kwargs.get('focus', True)

    @hexdi.inject('window', 'window.content')
    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget_class = args[0]
        if not widget_class: return None

        from .window import MainWindow
        window: MainWindow = args[1]

        from .content import WindowContent
        content: WindowContent = args[2]

        widget = widget_class(window)
        content.insertTab(position, widget, name, focus)
        return widget_class

    return wrapper1


def toolbar(*args, **kwargs):
    name = kwargs.get('name', 'New Tab')
    position = kwargs.get('position', 0)
    focus = kwargs.get('focus', True)

    @hexdi.inject('window.header')
    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget_class = args[0]
        if not widget_class: return None

        from .header import ToolbarWidget
        header: ToolbarWidget = args[1]

        widget = widget_class(header)
        header.insertTab(position, widget, name, focus)

        return widget_class

    return wrapper1
