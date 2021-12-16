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


@hexdi.inject('apprepo.downloader', 'console')
def validate(entity=None, options=None, callback=None, downloader=None, console=None):
    try:
        package = entity.get('package', None)
        if not package: raise Exception('Package is empty')
        yield console.comment("[found]: {}...".format(package))

        download_file = entity.get('file', None)
        if not download_file: raise Exception('File is empty')
        yield console.comment("[found]: {}...".format(download_file))

        download = downloader.download(download_file, callback if callback is not None else None)
        if not download: yield 'Can not download: {}'.format(download_file)

        assert (os.path.exists(download))

        os.chmod(download, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IRWXO | stat.S_IROTH)
        for line in validate_appimage(package, download):
            yield line

    except Exception as ex:
        yield console.error("[error]: {} - exception {}".format(package, ex))


@hexdi.inject('console')
def validate_appimage(package, appimage, console):
    with tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(appimage, stderr=stderr, stdout=stderr, preexec_fn=os.setsid)
        yield console.comment("[testing]: starting subprocess {}...".format(appimage))

        time.sleep(5)

        yield console.comment("[testing]: stopping subprocess {}...".format(appimage))
        if psutil.pid_exists(process.pid):
            os.killpg(process.pid, signal.SIGTERM)

        stderr.seek(0)

        output = str(stderr.read(), 'utf-8', errors='ignore')
        yield console.warning("[result]: {} - exit code: {}, stderr: {}...".format(package, process.returncode, output))

        os.remove(appimage)
        stderr.close()
