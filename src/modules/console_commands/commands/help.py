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

from modules.console import console


@console.task(name=['help'], description='Display help text')
@inject.params(application='console', logger='logger')
def help(options=None, arguments=None, application=None, logger=None):
    print("{}Usage: console.py [options] [arguments]{}".format(console.HEADER, console.ENDC))
    for (name, description, command) in application.get_commands():
        yield "{}{:<15}{}{}{}{}".format(console.OKGREEN, name, console.ENDC, console.COMMENT, description, console.ENDC)
