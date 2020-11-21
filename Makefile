SHELL := /usr/bin/bash
APPDIR := ./AppDir
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )
PWD := $(shell pwd)


all: clean

	mkdir -p $(PWD)/build
	mkdir -p $(PWD)/build/AppDir
	mkdir -p $(PWD)/build/AppDir/python
	mkdir -p $(PWD)/build/AppDir/apprepo
	mkdir -p $(PWD)/build/AppDir/vendor


	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/x86_64/os/Packages/python38-3.8.0-6.module_el8.2.0+317+61fa6e7d.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/x86_64/os/Packages/python38-devel-3.8.0-6.module_el8.2.0+317+61fa6e7d.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/aarch64/os/Packages/python38-pip-19.2.3-5.module_el8.2.0+317+61fa6e7d.noarch.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/x86_64/os/Packages/python38-setuptools-41.6.0-4.module_el8.2.0+317+61fa6e7d.noarch.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/x86_64/os/Packages/python38-libs-3.8.0-6.module_el8.2.0+317+61fa6e7d.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/openssl-libs-1.1.1c-15.el8.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/libffi-3.1-21.el8.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/AppStream/x86_64/os/Packages/intltool-0.51.0-11.el8.noarch.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/libgudev-232-4.el8.x86_64.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..


	cp --recursive --force $(PWD)/src/* $(PWD)/build/AppDir/apprepo
	cp --recursive --force $(PWD)/build/usr/* $(PWD)/build/AppDir/python
	cp --recursive --force $(PWD)/AppDir/AppRun $(PWD)/build/AppDir/AppRun
	chmod +x $(PWD)/build/AppDir/AppRun

	$(PWD)/build/AppDir/AppRun --python -m pip install  -r $(PWD)/requirements.txt --target=$(PWD)/build/AppDir/vendor --upgrade
	$(PWD)/build/AppDir/AppRun --python -m pip uninstall typing -y || true

	cp --force $(PWD)/AppDir/*.desktop $(PWD)/build/AppDir/
	cp --force $(PWD)/AppDir/*.png $(PWD)/build/AppDir/ || true
	cp --force $(PWD)/AppDir/*.svg $(PWD)/build/AppDir/ || true

	export ARCH=x86_64 && $(PWD)/bin/appimagetool.AppImage  $(PWD)/build/AppDir $(PWD)/apprepo.AppImage
	chmod +x $(PWD)/apprepo.AppImage

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r $(PWD)/requirements.txt

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/build
