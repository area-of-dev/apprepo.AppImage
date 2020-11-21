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

console = hexdi.resolve('console')
if not console: raise Exception('Console service not found')

@console.task(name=['help'], description='Display help text')
@hexdi.inject('console.application')
def help(options=None, arguments=None, application=None):
    yield console.header('Usage: console.py [options] [arguments]')
    for (name, description, command) in application.get_commands():
        yield "{:<23} {}".format(console.green(name), console.comment(description))
