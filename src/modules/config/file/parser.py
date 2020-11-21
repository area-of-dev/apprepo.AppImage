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
import configparser
import os


class ConfigFileParser(object):
    _parser = None

    def __init__(self, file=None):
        self._file = file
        self._parser = configparser.ConfigParser()
        if os.path.exists(self._file):
            self._parser.read(self._file)
            return None

        folder = os.path.dirname(self._file)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(self._file, 'w') as stream:
            self._parser.write(stream)
            stream.close()

        self._parser.read(self._file)
        return None

    def comment(self, section, text1='', text2=''):
        if not self._parser.has_section(section):
            self._parser.add_section(section)

        self._parser.set(section, "\n# %s" % text1, text2)

        with open(self._file, 'w') as stream:
            self._parser.write(stream)
            stream.close()

    def get(self, name, default=None):
        if not self.has(name):
            return self.set(name, default)

        section, option = name.split('.', 1)
        if not self._parser.has_section(section):
            return None

        if self._parser.has_option(section, option):
            return self._parser.get(section, option)
        return None

    def set(self, name, value=None):
        section, option = name.split('.', 1)

        if not self._parser.has_section(section):
            self._parser.add_section(section)

        self._parser.set(section, option, '%s' % value)
        with open(self._file, 'w') as stream:
            self._parser.write(stream)
            stream.close()
        return value

    def has(self, name):
        section, option = name.split('.', 1)

        if self._parser.has_section(section):
            return self._parser.has_option(section, option)

        return False
