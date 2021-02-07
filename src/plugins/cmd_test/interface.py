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
import os
import signal
import stat
import subprocess
import tempfile
import time

import hexdi
import psutil

from modules.cmd import console


@console.task(name=['test', 'check', 'validate'],
              description="Test compatibility of the selected "
                          "package with the current host")
def test_search_request(options=None, args=None):
    if args is None or not len(args):
        args = [None]

    for package in args:
        package = package.strip('\'"') if package else None
        for output in _test_search_request_element(package, options):
            yield output

    return 0


@hexdi.inject('apprepo', 'apprepo.downloader', 'console')
def _test_search_request_element(search=None, options=None, apprepo=None, downloader=None, console=None):
    yield console.comment("[processing]: search request {}...".format(search))

    collection = apprepo.search('') \
        if not search else \
        apprepo.package(search)

    for index, entity in enumerate(collection, start=1):

        try:
            package = entity.get('package', None)
            if not package: raise Exception('Package is empty')
            yield console.comment("[processing]: package {}...".format(package))

            download_file = entity.get('file', None)
            if not download_file: raise Exception('File is empty')
            yield console.comment("[processing]: file {}...".format(download_file))

            download = downloader.download(download_file)
            if not download: yield 'Can not download: {}'.format(download_file)

            assert (os.path.exists(download))

            os.chmod(download, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IRWXO | stat.S_IROTH)
            for line in _test_appimage(package, download):
                yield line
        except Exception as ex:
            yield console.error("[error]: {} - exception {}".format(package, ex))
            continue


@hexdi.inject('console')
def _test_appimage(package, appimage, console):
    with tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(appimage, stderr=stderr, stdout=stderr, preexec_fn=os.setsid)
        yield console.comment("[testing]: starting subprocess {}...".format(appimage))

        time.sleep(5)

        yield console.comment("[testing]: stopping subprocess {}...".format(appimage))
        if psutil.pid_exists(process.pid):
            os.killpg(process.pid, signal.SIGTERM)

        stderr.seek(0)

        output = str(stderr.read(), 'utf-8', errors='ignore')
        # distro.linux_distribution()
        yield console.warning("[result]: {} - exit code: {}, stderr: {}...".format(package, process.returncode, output))

        os.remove(appimage)
        stderr.close()
