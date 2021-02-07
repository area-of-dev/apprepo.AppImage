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
import glob
import os

import hexdi

from modules.appimage import appimage


def _reshapre(collection=[]):
    for source, destination in collection:
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)

        os.system("cp --recursive --force {} {}".format(source, destination))
        os.system("rm -rf {}".format(source.replace('/*', '')))

        yield source, destination


@appimage.shaper(priority=0)
@hexdi.inject('appimage')
def factory_shaper_bin(appdir_root, appdir_build, appimage):
    apprepo_bin = appimage.get_folder_bin(appdir_root)

    copypool = []

    copypool.append(('{}/usr/sbin/*'.format(appdir_build), apprepo_bin))
    copypool.append(('{}/usr/bin/*'.format(appdir_build), apprepo_bin))
    copypool.append(('{}/bin/*'.format(appdir_build), apprepo_bin))

    for output in _reshapre(copypool):
        yield output


@appimage.shaper(priority=10)
@hexdi.inject('appimage')
def factory_shaper_lib(appdir_root, appdir_build, appimage):
    apprepo_lib = appimage.get_folder_lib(appdir_root)

    copypool = []

    copypool.append(('{}/usr/lib/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/usr/lib64/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/lib64/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/lib/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/x86_64-linux-gnu/*'.format(apprepo_lib), apprepo_lib))

    for output in _reshapre(copypool):
        yield output

    command = []
    command.append("ln -s ./lib64 {}/lib".format(appdir_root))
    command.append("ln -s ../lib64 {}/lib64/x86_64-linux-gnu".format(appdir_root))

    os.system(" && ".join(command))
    yield None, None


@appimage.shaper(priority=20)
@hexdi.inject('appimage')
def factory_shaper_libexec(appdir_root, appdir_build, appimage):
    apprepo_libexec = appimage.get_folder_libexec(appdir_root)
    apprepo_lib = appimage.get_folder_lib(appdir_root)

    copypool = []

    copypool.append(('{}/lib64/libexec/*'.format(appdir_build), apprepo_libexec))
    copypool.append(('{}/lib/libexec/*'.format(appdir_build), apprepo_libexec))
    copypool.append(('{}/libexec/*'.format(apprepo_lib), apprepo_libexec))

    for output in _reshapre(copypool):
        yield output


@appimage.shaper(priority=20)
@hexdi.inject('appimage')
def factory_shaper_share(appdir_root, appdir_build, appimage):
    apprepo_share = appimage.get_folder_share(appdir_root)

    copypool = []

    copypool.append(('{}/usr/share/*'.format(appdir_build), apprepo_share))
    copypool.append(('{}/share/*'.format(appdir_build), apprepo_share))
    copypool.append(('{}/share/applications/*.desktop'.format(appdir_root), appdir_root))

    for output in _reshapre(copypool):
        yield output


@appimage.shaper(priority=100)
@hexdi.inject('appimage')
def factory_shaper_glib_schemas(appdir_root, appdir_build, appimage):
    apprepo_lib = appimage.get_folder_lib(appdir_root)
    apprepo_share = appimage.get_folder_share(appdir_root)
    apprepo_bin = appimage.get_folder_bin(appdir_root)

    command = []
    command.append("export XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:{}".format(apprepo_share))
    command.append("export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:{}".format(apprepo_lib))

    command.append("{}/glib-2.0/glib-compile-schemas {}/glib-2.0/schemas/ > /dev/null 2>&1".format(
        apprepo_lib, apprepo_share
    ))

    command.append("{}/glib-compile-schemas {}/glib-2.0/schemas/ > /dev/null 2>&1".format(
        apprepo_bin, apprepo_share
    ))

    os.system(" && ".join(command))
    yield None, None


@appimage.shaper(priority=100)
@hexdi.inject('appimage')
def factory_shaper_mime(appdir_root, appdir_build, appimage):
    apprepo_lib = appimage.get_folder_lib(appdir_root)
    apprepo_share = appimage.get_folder_share(appdir_root)
    apprepo_bin = appimage.get_folder_bin(appdir_root)

    command = []
    command.append("export XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:{}".format(apprepo_share))
    command.append("export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:{}".format(apprepo_lib))
    command.append("{}/update-mime-database {}/mime".format(apprepo_bin, apprepo_share))

    os.system(" && ".join(command))
    yield None, None


@appimage.shaper(priority=100)
@hexdi.inject('appimage')
def factory_shaper_gtk_immodules(appdir_root, appdir_build, appimage):
    apprepo_lib = appimage.get_folder_lib(appdir_root)
    apprepo_bin = appimage.get_folder_bin(appdir_root)

    GTK_IM_MODULEDIR = "{}/gtk-3.0/3.0.0/immodules".format(apprepo_lib)
    GTK_IM_MODULE_FILE = "{}/gtk-3.0/3.0.0/immodules.cache".format(apprepo_lib)
    if not os.path.exists(GTK_IM_MODULEDIR) or not os.path.isdir(GTK_IM_MODULEDIR):
        yield None, None

    command = []
    command.append("export GTK_IM_MODULE_FILE={}".format(GTK_IM_MODULE_FILE))

    modules = []
    for path in glob.glob("{}/*.so".format(GTK_IM_MODULEDIR)):
        modules.append(path)

    modules = " ".join(modules)
    GTK_IM_MODULE_BINARY = "{}/gtk-query-immodules".format(apprepo_bin)
    if os.path.exists(GTK_IM_MODULE_BINARY) and os.path.isfile(GTK_IM_MODULE_BINARY):
        command.append("{} --update-cache {}".format(GTK_IM_MODULE_BINARY, modules))

    GTK_IM_MODULE_BINARY = "{}/gtk-query-immodules-3.0".format(apprepo_bin)
    if os.path.exists(GTK_IM_MODULE_BINARY) and os.path.isfile(GTK_IM_MODULE_BINARY):
        command.append("{} --update-cache {}".format(GTK_IM_MODULE_BINARY, modules))

    GTK_IM_MODULE_BINARY = "{}/libgtk-3-0/gtk-query-immodules".format(apprepo_lib)
    if os.path.exists(GTK_IM_MODULE_BINARY) and os.path.isfile(GTK_IM_MODULE_BINARY):
        command.append("{} --update-cache {}".format(GTK_IM_MODULE_BINARY, modules))

    GTK_IM_MODULE_BINARY = "{}/libgtk-3-0/gtk-query-immodules-3.0".format(apprepo_lib)
    if os.path.exists(GTK_IM_MODULE_BINARY) and os.path.isfile(GTK_IM_MODULE_BINARY):
        command.append("{} --update-cache {}".format(GTK_IM_MODULE_BINARY, modules))

    os.system(" && ".join(command))

    if os.path.exists(GTK_IM_MODULE_FILE):
        with open(GTK_IM_MODULE_FILE, 'r+') as stream:
            content = stream.read()
            content = content.replace("{}/".format(GTK_IM_MODULEDIR), '')
            content = content.replace(GTK_IM_MODULEDIR, '')
            stream.close()

            with open(GTK_IM_MODULE_FILE, 'w') as stream:
                stream.write(content)
                stream.close()

    yield None, None


@appimage.shaper(priority=100)
@hexdi.inject('appimage')
def factory_shaper_gdk_pixbuf_loaders(appdir_root, appdir_build, appimage):
    apprepo_lib = appimage.get_folder_lib(appdir_root)
    apprepo_share = appimage.get_folder_share(appdir_root)
    apprepo_bin = appimage.get_folder_bin(appdir_root)

    GDK_PIXBUF_MODULEDIR = "{}/gdk-pixbuf-2.0/2.10.0/loaders".format(apprepo_lib)
    GDK_PIXBUF_MODULE_FILE = "{}/gdk-pixbuf-2.0/2.10.0/loaders.cache".format(apprepo_lib)
    if not os.path.exists(GDK_PIXBUF_MODULEDIR) or not os.path.isdir(GDK_PIXBUF_MODULEDIR):
        yield None, None

    command = []
    command.append("export XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:{}".format(apprepo_share))
    command.append("export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:{}".format(apprepo_lib))
    command.append("export GDK_PIXBUF_MODULEDIR={}".format(GDK_PIXBUF_MODULEDIR))

    GDK_PIXBUF_QUERY_LOADER = "{}/gdk-pixbuf-query-loaders-64".format(apprepo_bin)
    if os.path.exists(GDK_PIXBUF_QUERY_LOADER) and os.path.isfile(GDK_PIXBUF_QUERY_LOADER):
        command.append("{} > {}".format(GDK_PIXBUF_QUERY_LOADER, GDK_PIXBUF_MODULE_FILE))

    GDK_PIXBUF_QUERY_LOADER = "{}/gdk-pixbuf-query-loaders".format(apprepo_bin)
    if os.path.exists(GDK_PIXBUF_QUERY_LOADER) and os.path.isfile(GDK_PIXBUF_QUERY_LOADER):
        command.append("{} > {}".format(GDK_PIXBUF_QUERY_LOADER, GDK_PIXBUF_MODULE_FILE))

    GDK_PIXBUF_QUERY_LOADER = "{}/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders".format(apprepo_lib)
    if os.path.exists(GDK_PIXBUF_QUERY_LOADER) and os.path.isfile(GDK_PIXBUF_QUERY_LOADER):
        command.append("{} > {}".format(GDK_PIXBUF_QUERY_LOADER, GDK_PIXBUF_MODULE_FILE))

    GDK_PIXBUF_QUERY_LOADER = "{}/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders-64".format(apprepo_lib)
    if os.path.exists(GDK_PIXBUF_QUERY_LOADER) and os.path.isfile(GDK_PIXBUF_QUERY_LOADER):
        command.append("{} > {}".format(GDK_PIXBUF_QUERY_LOADER, GDK_PIXBUF_MODULE_FILE))

    os.system(" && ".join(command))

    if os.path.exists(GDK_PIXBUF_MODULE_FILE):
        with open(GDK_PIXBUF_MODULE_FILE, 'r+') as stream:
            content = stream.read()
            content = content.replace("{}/".format(GDK_PIXBUF_MODULEDIR), '')
            content = content.replace(GDK_PIXBUF_MODULEDIR, '')
            stream.close()

            with open(GDK_PIXBUF_MODULE_FILE, 'w') as stream:
                stream.write(content)
                stream.close()

    yield None, None
