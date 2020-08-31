SHELL := /usr/bin/bash
APPDIR := ./AppDir
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )
PWD := $(shell pwd)

all: init appimage clean

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r $(PWD)/requirements.txt


appimage: clean
	source $(PWD)/venv/bin/activate && python3 -O -m PyInstaller src/console.py --distpath $(APPDIR) --name application --noconfirm
	cp -r ./src/modules $(APPDIR)/application
	cp -r ./src/lib $(APPDIR)/application

	bin/appimagetool.AppImage  ./AppDir apprepo.AppImage
	@echo "done: Apprepo.AppImage"

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/application
	rm -rf ${APPDIR}/opt
