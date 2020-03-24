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
	source $(PWD)/venv/bin/activate && python3 -O -m PyInstaller src/main.py --distpath $(APPDIR) --name application --noconfirm
	cp -r ./src/icons $(APPDIR)/application
	cp -r ./src/lib $(APPDIR)/application
	cp -r ./src/modules $(APPDIR)/application
	cp -r ./src/plugins $(APPDIR)/application
	cp -r ./src/themes $(APPDIR)/application

	bin/appimagetool-x86_64.AppImage  ./AppDir bin/AOD-Notes.AppImage
	@echo "done: bin/AOD-Notes.AppImage"

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/application
	rm -rf ${APPDIR}/opt
