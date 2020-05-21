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


class Console(object):
    # api = 'http://localhost:8000/rest/api'

    def info(self, options=None, args=None):
        """
        List all installed application
        :param args:
        :param options:
        :return:
        """
        from .task import info
        for entity in info.main(options, args):
            yield entity

    def synchronize(self, options=None, args=None):
        """
        Synchronize all found Applications with the system.
        Generate .desktop files and the icons and put them into system folders

        :param args:
        :param options:
        :return:
        """
        from .task import synchronize
        for entity in synchronize.main(options, args):
            yield entity

    def cleanup(self, options=None, args=None):
        """
        Synchronize all found Applications with the system.
        Generate .desktop files and the icons and put them into system folders

        :param args:
        :param options:
        :return:
        """
        from .task import cleanup
        for entity in cleanup.main(args, options):
            yield entity

    def search(self, options=None, args=None):
        """
        Find application in the repository
        :param options:
        :param args:
        :return:
        """
        from .task import search
        for entity in search.main(options, args):
            yield entity

        # if string is None or not len(string):
        #     raise Exception('search string can not be empty')
        #
        # task = SearchTask('{}/package'.format(self.api))
        #
        # for entity in task.process(string):
        #     print("{:>s} ({:>s}) - {:>s}".format(
        #         entity['name'] or 'Unknown',
        #         entity['version'] or 'Unknown',
        #         entity['description'] or 'Unknown'
        #     ))

    def install(self, options=None, args=None):
        """
        Install application from the repository
        :param options:
        :param args:
        :return:
        """
        from .task import install
        for entity in install.main(options, args):
            yield entity

        # if string is None or not len(string):
        #     raise Exception('search string can not be empty')

    #
    #     task = InstallPackageTask('{}/package'.format(self.api))
    #     for entity in task.process(string, options.force, options.systemwide):
    #         yield "Installed: {:>s}, latest version: {}, from: {}".format(
    #             entity['name'] or 'Unknown',
    #             entity['version'] or 'Unknown',
    #             entity['file'] or 'Unknown'
    #         )

    def uninstall(self, options=None, args=None):
        """
        Uninstall application from local system
        :param options:
        :param args:
        :return:
        """
        from .task import uninstall
        for entity in uninstall.main(options, args):
            yield entity

    #     if string is None or not len(string):
    #         raise Exception('search string can not be empty')
    #
    #     task = UninstallPackageTask('{}/package'.format(self.api))
    #     for entity in task.process(string, options):
    #         yield "Uninstalled: {:>s} - latest version: {} ({})".format(
    #             entity['package'] or 'Unknown',
    #             entity['name'] or 'Unknown',
    #             entity['version'] or 'Unknown',
    #         )
    #

    def update(self, options=None, args=None):
        """
        Update selected package or all packages
        if no packages were selected
        :param options:
        :param args:
        :return:
        """
        from .task import update
        for entity in update.main(options, args):
            yield entity

    #     from .task.sync import SynchronizePackageTask
    #
    #     task = SynchronizePackageTask('{}/package'.format(self.api))
    #     for entity in task.process(string, options):
    #         assert ('name' in entity.keys())
    #         assert ('package' in entity.keys())
    #         assert ('version' in entity.keys())
    #         assert ('file' in entity.keys())
    #
    #         yield "Found: {:>s} - recognized as {:>s}, latest version: {}, download: {}".format(
    #             entity['package'] or 'Unknown',
    #             entity['name'] or 'Unknown',
    #             entity['version'] or 'Unknown',
    #             entity['file'] or 'Unknown',
    #         )
    #
    #         assert ('slug' in entity.keys())
    #         if entity['slug'] is None: continue
    #         for output in self.install_package(entity['slug'], options):
    #             yield output

    def upload(self, options=None, args=None):
        """
        Upload new version of the package into repository
        :param options:
        :param args:
        :return:
        """
        from .task import upload
        for entity in upload.main(options, args):
            yield entity

    #     if path is None or not len(path):
    #         raise Exception('File path can not be empty')
    #
    #     if not os.path.exists(path) or os.path.isdir(path):
    #         raise Exception('File does not exist: {}'.format(path))
    #
    #     if options is None or not options:
    #         raise Exception('Please setup version options')
    #
    #     if options.version_token is None or not len(options.version_token):
    #         raise Exception('token not found')
    #
    #     if options.version_description is None or not len(options.version_description):
    #         raise Exception('description not found')
    #
    #     if options.version_name is None or not len(options.version_name):
    #         raise Exception('name not found')
    #
    #     url_initialize = "{}/package/upload/initialize/".format(self.api)
    #     url_finalize = '{}/package/upload/complete/finalize/'.format(self.api)
    #     task = VersionUploadTask(url_initialize, url_finalize)
    #
    #     result = task.upload(path, {
    #         'token': options.version_token,
    #         'description': options.version_description,
    #         'name': options.version_name,
    #     })
    #
    #     if result is None or not result:
    #         raise Exception('Result can not be empty')
    #
    #     yield 'Uploaded: {} {} - {}, {}'.format(
    #         result['package'] or 'Unknown',
    #         result['version'] or 'Unknown',
    #         result['description'] or 'Unknown',
    #         path or 'Unknown'
    #     )
    #
    # def search_group(self, string=None, options=None):
    #     if string is None or not len(string):
    #         raise Exception('search string can not be empty')
    #
    #     task = SearchTask('{}/package/groups'.format(self.api))
    #     for entity in task.process(string):
    #         yield "{:>s} - {:>s}".format(
    #             entity['name'] or 'Unknown',
    #             entity['description'] or 'Unknown'
    #         )
    #
