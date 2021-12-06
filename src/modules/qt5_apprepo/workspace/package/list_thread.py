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
from urllib import request

from PyQt5 import QtCore


class PackageImageThread(QtCore.QThread):
    imageLoaded = QtCore.pyqtSignal(object)

    def __init__(self):
        super(PackageImageThread, self).__init__()
        self.stop = False
        self.images = []

    def append(self, image):
        self.images.append(image)
        return self

    def clear(self):
        self.images = []
        return self

    def run(self):

        while True:
            for (image, callback) in self.images:
                if not len(self.images): break

                url = image.get('url', None)
                if not url: continue

                data = request.urlopen(url).read()
                self.imageLoaded.emit((data, callback))

            if self.stop: break
            QtCore.QThread.msleep(500)

    def terminate(self) -> None:
        self.stop = True
        super().terminate()

    def __del__(self):
        self.wait()
