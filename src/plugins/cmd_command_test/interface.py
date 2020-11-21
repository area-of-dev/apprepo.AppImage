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
import pty
import signal
import stat
import subprocess
import time

import hexdi
import psutil


@hexdi.inject('console')
def _check(appimage, console):
    yield "[{}]: starting subprocess {}...".format(console.blue('testing'), appimage)

    err_r, out_r = pty.openpty()
    process = subprocess.Popen(appimage, stderr=err_r, stdout=err_r, preexec_fn=os.setsid)

    time.sleep(5)

    while not process.poll():
        yield console.comment("[testing]: stopping subprocess {}...".format(appimage))
        if not psutil.pid_exists(process.pid):
            break

        os.killpg(process.pid, signal.SIGTERM)
        break

    output = str(os.read(err_r, 1024 * 1024), 'utf-8', errors='ignore')
    yield console.warning("[testing]: status {}, stderr: {}...".format(process.returncode, output))
    os.remove(appimage)


@hexdi.inject('appimagetool', 'apprepo', 'downloader', 'console')
def _test_action(search=None, options=None, appimagetool=None, apprepo=None, downloader=None, console=None):
    yield console.comment("[processing]: search request {}...".format(search))

    collection = apprepo.search('') \
        if not search else \
        apprepo.package(search)

    for index, entity in enumerate(collection, start=1):

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
        for output in _check(download):
            yield output


console = hexdi.resolve('console')
if not console: raise Exception('Console service not found')
description = "Test compatibility of the selected package with the current host"


@console.task(name=['test', 'check', 'validate'], description=description)
def test_action(options=None, args=None):
    if args is None or not len(args):
        args = [None]

    for package in args:
        package = package.strip('\'"') if package else None
        for output in _test_action(package, options):
            yield output
    return 0
