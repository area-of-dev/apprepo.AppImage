SHELL := /usr/bin/bash
APPDIR := ./AppDir
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )
PWD := $(shell pwd)


all: clean


	mkdir -p $(PWD)/build

	source $(PWD)/venv/bin/activate && python3 $(PWD)/src/console.py --destination=$(PWD)/build appdir apprepo python3.8 \
													python3.8-dev python3.8-psutil python3.8-setuptools python3-pip python3-dnf python3-apt \
													openssl libffi7 intltool libgudev-1.0-0 libffi libgudev \

	echo '#cd $${OWD}' >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo 'case "$${1}" in' >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo "  '--python') exec \$${APPDIR}/bin/python3.8 \$${*:2} ;;" >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo "  '--desktop') \$${APPDIR}/bin/python3.8 \$${APPDIR}/apprepo/main.py \$${*:2} ;;" >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo '  *)   $${APPDIR}/bin/python3.8 $${APPDIR}/apprepo/console.py $${@} ;;' >> $(PWD)/build/Apprepo.AppDir/AppRun
	echo 'esac' >> $(PWD)/build/Apprepo.AppDir/AppRun
	sed -i 's/#APPDIR=`pwd`/APPDIR=`dirname \$${0}`/' $(PWD)/build/Apprepo.AppDir/AppRun

	mkdir -p $(PWD)/build/Apprepo.AppDir/apprepo
	mkdir -p $(PWD)/build/Apprepo.AppDir/vendor

	cp --recursive --force $(PWD)/src/* $(PWD)/build/Apprepo.AppDir/apprepo
	chmod +x $(PWD)/build/Apprepo.AppDir/AppRun
	cd $(PWD)/build/Apprepo.AppDir && ./AppRun --python -m pip install  -r $(PWD)/requirements.txt --target=./vendor --upgrade
	cd $(PWD)/build/Apprepo.AppDir && ./AppRun --python -m pip uninstall typing -y || true

	sed -i 's/APPDIR=`dirname \$${0}`/#APPDIR=`dirname \$${0}`/' $(PWD)/build/Apprepo.AppDir/AppRun

	rm -f $(PWD)/build/Apprepo.AppDir/*.desktop

	cp --force $(PWD)/AppDir/*.desktop $(PWD)/build/Apprepo.AppDir/
	cp --force $(PWD)/AppDir/*.png $(PWD)/build/Apprepo.AppDir/ || true
	cp --force $(PWD)/AppDir/*.svg $(PWD)/build/Apprepo.AppDir/ || true

	export ARCH=x86_64 && $(PWD)/bin/appimagetool.AppImage $(PWD)/build/Apprepo.AppDir $(PWD)/apprepo.AppImage
	chmod +x $(PWD)/apprepo.AppImage


init:
	rm -rf $(PWD)/venv
	python3.8 -m venv $(PWD)/venv --system-site-packages
	source $(PWD)/venv/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r $(PWD)/requirements.txt

clean:
	rm -rf ${PWD}/build

