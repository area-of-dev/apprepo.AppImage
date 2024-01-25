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
SHELL := /usr/bin/bash
APPDIR := ./AppDir
PWD := $(shell pwd)


all: clean init


	mkdir -p $(PWD)/build

	source $(PWD)/venv/bin/activate && python3 ./src/console.py --destination=$(PWD)/build appdir apprepo python3 python3-psutil \
										python3-setuptools python3-pip python3-dnf python3-apt \
										openssl libffi7 intltool libgudev-1.0-0 libffi libgudev

	echo '#cd $${OWD}'                                                                      >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo 'case "$${1}" in'                                                                  >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo "  '--python') exec \$${APPDIR}/bin/python3* \$${*:2} ;;"                          >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo "  '--desktop') \$${APPDIR}/bin/python3* \$${APPDIR}/apprepo/main.py \$${*:2} ;;"  >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo '  *)   $${APPDIR}/bin/python3* $${APPDIR}/apprepo/console.py $${@} ;;'            >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo 'esac'                                                                             >> $(PWD)/build/Apprepo.AppDir/AppRun
	
	sed -i 's/#APPDIR=`pwd`/APPDIR=`dirname \$${0}`/' $(PWD)/build/Apprepo.AppDir/AppRun

	mkdir -p $(PWD)/build/Apprepo.AppDir/apprepo
	mkdir -p $(PWD)/build/Apprepo.AppDir/vendor

	cp --recursive --force $(PWD)/src/* $(PWD)/build/Apprepo.AppDir/apprepo
	chmod +x $(PWD)/build/Apprepo.AppDir/AppRun
	cd $(PWD)/build/Apprepo.AppDir && ./AppRun --python -m pip install  -r $(PWD)/requirements.txt --target=./vendor --upgrade
	cd $(PWD)/build/Apprepo.AppDir && ./AppRun --python -m pip uninstall typing -y || true

	sed -i 's/APPDIR=`dirname \$${0}`/#APPDIR=`dirname \$${0}`/' $(PWD)/build/Apprepo.AppDir/AppRun

	rm --recursive --force $(PWD)/build/Apprepo.AppDir/*.desktop                 || true
	# rm --recursive --force $(PWD)/build/Boilerplate.AppDir/lib64/libstdc++.so.6* || true

	cp --force $(PWD)/AppDir/*.desktop $(PWD)/build/Apprepo.AppDir/
	cp --force $(PWD)/AppDir/*.png $(PWD)/build/Apprepo.AppDir/ || true
	cp --force $(PWD)/AppDir/*.svg $(PWD)/build/Apprepo.AppDir/ || true

	export ARCH=x86_64 && $(PWD)/bin/appimagetool.AppImage $(PWD)/build/Apprepo.AppDir $(PWD)/apprepo.AppImage
	chmod +x $(PWD)/apprepo.AppImage


init:
	rm -rf $(PWD)/venv
	python3 -m venv $(PWD)/venv --system-site-packages
	source $(PWD)/venv/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r $(PWD)/requirements.txt

	wget https://github.com/area-of-dev/apprepo.AppImage/releases/download/latest/apprepo.AppImage \
		--output-document=$(PWD)/bin/Apprepo.AppImage
	chmod +x $(PWD)/bin/Apprepo.AppImage

	wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage \
		--output-document=$(PWD)/bin/appimagetool.AppImage
	chmod +x $(PWD)/bin/appimagetool.AppImage


clean:
	rm -rf ${PWD}/build
	rm -rf ${PWD}/*.AppImage

