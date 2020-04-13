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
import os

from .task.search import SearchTask
from .task.install import InstallPackageTask
from .task.uninstall import UninstallPackageTask
from .task.upload import VersionUploadTask
from .task.synchronize import SynchronizePackageTask


class Console(object):
    api = 'http://localhost:8000/rest/api'

    def upload_version(self, path=None, options=None):
        if path is None or not len(path):
            raise Exception('File path can not be empty')

        if not os.path.exists(path) or os.path.isdir(path):
            raise Exception('File does not exist: {}'.format(path))

        if options is None or not options:
            raise Exception('Please setup version options')

        if options.version_token is None or not len(options.version_token):
            raise Exception('token not found')

        if options.version_description is None or not len(options.version_description):
            raise Exception('description not found')

        if options.version_name is None or not len(options.version_name):
            raise Exception('name not found')

        url_initialize = "{}/package/upload/initialize/".format(self.api)
        url_finalize = '{}/package/upload/complete/finalize/'.format(self.api)
        task = VersionUploadTask(url_initialize, url_finalize)

        result = task.upload(path, {
            'token': options.version_token,
            'description': options.version_description,
            'name': options.version_name,
        })

        if result is None or not result:
            raise Exception('Result can not be empty')

        yield 'Uploaded: {} {} - {}, {}'.format(
            result['package'] or 'Unknown',
            result['version'] or 'Unknown',
            result['description'] or 'Unknown',
            path or 'Unknown'
        )

    def search_package(self, string=None, options=None):
        if string is None or not len(string):
            raise Exception('search string can not be empty')

        task = SearchTask('{}/package'.format(self.api))

        for entity in task.process(string):
            print("{:>s} ({:>s}) - {:>s}".format(
                entity['name'] or 'Unknown',
                entity['version'] or 'Unknown',
                entity['description'] or 'Unknown'
            ))

    def search_group(self, string=None, options=None):
        if string is None or not len(string):
            raise Exception('search string can not be empty')

        task = SearchTask('{}/package/groups'.format(self.api))
        for entity in task.process(string):
            yield "{:>s} - {:>s}".format(
                entity['name'] or 'Unknown',
                entity['description'] or 'Unknown'
            )

    def install_package(self, string=None, options=None):
        if string is None or not len(string):
            raise Exception('search string can not be empty')

        task = InstallPackageTask('{}/package'.format(self.api))
        for entity in task.process(string, options.force, options.systemwide):
            yield "Installed: {:>s}, latest version: {}, from: {}".format(
                entity['name'] or 'Unknown',
                entity['version'] or 'Unknown',
                entity['file'] or 'Unknown'
            )

    def uninstall_package(self, string=None, options=None):
        if string is None or not len(string):
            raise Exception('search string can not be empty')

        task = UninstallPackageTask('{}/package'.format(self.api))
        for entity in task.process(string, options):
            yield "Uninstalled: {:>s} - latest version: {} ({})".format(
                entity['package'] or 'Unknown',
                entity['name'] or 'Unknown',
                entity['version'] or 'Unknown',
            )

    def synchronize_package(self, string=None, options=None):

        task = SynchronizePackageTask('{}/package'.format(self.api))
        for entity in task.process(string, options):
            assert ('name' in entity.keys())
            assert ('package' in entity.keys())
            assert ('version' in entity.keys())
            assert ('file' in entity.keys())

            yield "Found: {:>s} - recognized as {:>s}, latest version: {}, download: {}".format(
                entity['package'] or 'Unknown',
                entity['name'] or 'Unknown',
                entity['version'] or 'Unknown',
                entity['file'] or 'Unknown',
            )

            assert ('slug' in entity.keys())
            if entity['slug'] is None: continue
            for output in self.install_package(entity['slug'], options):
                yield output
