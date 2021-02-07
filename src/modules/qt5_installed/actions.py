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


@hexdi.inject('console.application')
def on_action_synchronize(event=None, cmd=None):
    command = cmd.get_command('synchronize')
    for entity in command(None, []):
        print(entity)


@hexdi.inject('console.application')
def on_action_cleanup(event=None, cmd=None):
    command = cmd.get_command('cleanup')
    for entity in command(None, []):
        print(entity)


@hexdi.inject('console.application')
def on_action_update(event=None, cmd=None):
    command = cmd.get_command('update')
    for entity in command(None, []):
        print(entity)
