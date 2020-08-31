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
# -*- coding: utf-8 -*-
# Copyright 2018 Alex Woroschilow (alex.woroschilow@gmail.com)
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
import inject

HEADER = '\033[95m'
COMMENT = '\033[90m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def header(text=None):
    return "{}{}{}".format(HEADER, text, ENDC)


def comment(text=None):
    return "{}{}{}".format(COMMENT, text, ENDC)


def green(text=None):
    return "{}{}{}".format(OKGREEN, text, ENDC)


def blue(text=None):
    return "{}{}{}".format(OKBLUE, text, ENDC)


def warning(text=None):
    return "{}{}{}".format(WARNING, text, ENDC)


def error(text=None):
    return "{}{}{}".format(FAIL, text, ENDC)


@inject.params(console='console')
def task(*args, **kwargs):
    name = kwargs.get('name', None)
    if not name: raise ValueError('Command name can not be empty')
    description = kwargs.get('description', None)
    console: ApplicationConsole = \
        kwargs.get('console')

    def wrapper1(*args, **kwargs):

        if type(name) is list or type(name) is tuple:
            for alias in name:
                console.add_command(alias, args[0], description)

        if type(name) is str:
            console.add_command(name, args[0], description)

        def wrapper2(*args, **kwargs):
            function = console.get_command(name)
            return function(*args)

        return wrapper2

    return wrapper1


class ApplicationConsole(object):

    def __init__(self):
        self.commands = {}

    def add_command(self, name=None, function=None, description=None):
        if name in self.commands.keys(): raise ValueError('Command already exists')
        self.commands[name] = (function, description)

    def get_command(self, name=None, default=None):
        if name not in self.commands.keys(): raise ValueError('Command not found')
        function, description = self.commands.get(name or default)
        return function

    def get_commands(self):
        for name in self.commands.keys():
            (function, description) = self.commands[name]
            yield (name, description, function)
