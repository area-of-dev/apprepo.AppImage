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

factory = hexdi.resolve('appimage')


def _get_folders(enterpoint):
    pool = [enterpoint]

    while len(pool):
        location = pool.pop()
        yield location
        for path in glob.glob("{}**/*".format(location), recursive=True):
            if os.path.isfile(path):
                continue

            if os.path.islink(path):
                continue

            if path.find('__pycache__') == -1:
                pool.append(path)


@factory.apprun(priority=0)
@hexdi.inject('appimage')
def apprun_header(appdir_root, appimage):
    return ["""#! /bin/bash    
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
#APPDIR=`pwd`\n\n"""]


@factory.apprun(priority=20)
@hexdi.inject('appimage')
def apprun_path_bin(appdir_root, appimage):
    content = []

    apprepo_bin = factory.get_folder_bin(appdir_root)
    if not os.path.exists(apprepo_bin) or not os.path.isdir(apprepo_bin):
        return content

    for path in _get_folders(apprepo_bin):
        path_local = path.replace(appdir_root, '')
        content.append('PATH=${{PATH}}:${{APPDIR}}{}'.format(path_local))

    content.append("export PATH=${PATH}\n")

    return content


@factory.apprun(priority=30)
@hexdi.inject('appimage')
def apprun_path_libexec(appdir_root, appimage):
    content = []

    apprepo_libexec = appimage.get_folder_libexec(appdir_root)
    if not os.path.exists(apprepo_libexec) or not os.path.isdir(apprepo_libexec):
        return content

    for path in _get_folders(apprepo_libexec):
        path_local = path.replace(appdir_root, '')
        content.append('PATH=${{PATH}}:${{APPDIR}}{}'.format(path_local))

    content.append("export PATH=${PATH}\n")

    return content


@factory.apprun(priority=40)
@hexdi.inject('appimage')
def apprun_path_ld_library_path(appdir_root, appimage):
    content = []

    apprepo_lib = appimage.get_folder_lib(appdir_root)
    if not os.path.exists(apprepo_lib) or not os.path.isdir(apprepo_lib):
        return content

    path_local = apprepo_lib.replace(appdir_root, '')

    content.append('GDK_PIXBUF_MODULEDIR=${{APPDIR}}{}/gdk-pixbuf-2.0/2.10.0/loaders'.format(path_local))
    content.append("export GDK_PIXBUF_MODULEDIR=${GDK_PIXBUF_MODULEDIR}\n")

    content.append('GDK_PIXBUF_MODULE_FILE=${{APPDIR}}{}/gdk-pixbuf-2.0/2.10.0/loaders.cache'.format(path_local))
    content.append("export GDK_PIXBUF_MODULE_FILE=${GDK_PIXBUF_MODULE_FILE}\n")

    content.append('GTK_PATH=${{GTK_PATH}}:${{APPDIR}}{}/gtk-2.0'.format(path_local))
    content.append('GTK_PATH=${{GTK_PATH}}:${{APPDIR}}{}/gtk-3.0'.format(path_local))
    content.append("export GTK_PATH=${GTK_PATH}\n")

    content.append('GTK_IM_MODULE_FILE=${{APPDIR}}{}/gtk-3.0/3.0.0/immodules.cache'.format(path_local))
    content.append("export GTK_IM_MODULE_FILE=${GTK_IM_MODULE_FILE}\n")

    content.append('PANGO_LIBDIR=${{APPDIR}}{}'.format(path_local))
    content.append("export PANGO_LIBDIR=${PANGO_LIBDIR}\n")

    for path in _get_folders(apprepo_lib):
        path_local = path.replace(appdir_root, '')
        content.append('LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:${{APPDIR}}{}'.format(path_local))

    content.append('LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:${{APPDIR}}{}/gdk-pixbuf-2.0/loaders'.format(path_local))
    content.append("export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}\n")

    return content


@factory.apprun(priority=50)
@hexdi.inject('appimage')
def apprun_path_gi_typelib_path(appdir_root, appimage):
    content = []

    apprepo_libgi = factory.get_folder_libpython(appdir_root)
    if not os.path.exists(apprepo_libgi) or not os.path.isdir(apprepo_libgi):
        return content

    for path in _get_folders(apprepo_libgi):
        path_local = path.replace(appdir_root, '')
        content.append('GI_TYPELIB_PATH=${{GI_TYPELIB_PATH}}:${{APPDIR}}{}'.format(path_local))

    content.append("export GI_TYPELIB_PATH=${GI_TYPELIB_PATH}\n")

    return content


@factory.apprun(priority=60)
@hexdi.inject('appimage')
def apprun_path_qt_plugin_path(appdir_root, appimage):
    content = []

    apprepo_libqt5 = factory.get_folder_libqt5(appdir_root)
    if not os.path.exists(apprepo_libqt5) or not os.path.isdir(apprepo_libqt5):
        return content

    for path in _get_folders(apprepo_libqt5):
        path_local = path.replace(appdir_root, '')
        content.append('QT_PLUGIN_PATH=${{QT_PLUGIN_PATH}}:${{APPDIR}}{}'.format(path_local))

    content.append("export QT_PLUGIN_PATH=${QT_PLUGIN_PATH}\n")

    return content


@factory.apprun(priority=70)
@hexdi.inject('appimage')
def apprun_path_perl5lib(appdir_root, appimage):
    content = []

    apprepo_libperl = factory.get_folder_libperl5(appdir_root)
    if not os.path.exists(apprepo_libperl) or not os.path.isdir(apprepo_libperl):
        return content

    for path in _get_folders(apprepo_libperl):
        path_local = path.replace(appdir_root, '')
        content.append('PERL5LIB=${{PERL5LIB}}:${{APPDIR}}{}'.format(path_local))

    content.append("export PERL5LIB=${PERL5LIB}\n")

    return content


@factory.apprun(priority=80)
@hexdi.inject('appimage')
def apprun_path_pythonpath(appdir_root, appimage):
    content = []

    apprepo_lib = appimage.get_folder_lib(appdir_root)
    if not os.path.exists(apprepo_lib) or not os.path.isdir(apprepo_lib):
        return content

    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.6')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.6/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.6/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.6/lib-dynload')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.8')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.8/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.8/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.8/lib-dynload')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.9')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.9/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.9/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib64/python3.9/lib-dynload')

    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/vendor')
    content.append("export PYTHONPATH=${PYTHONPATH}\n")

    return content


@factory.apprun(priority=90)
@hexdi.inject('appimage')
def apprun_path_xdg_data_dirs(appdir_root, appimage):
    content = []

    apprepo_share = appimage.get_folder_share(appdir_root)
    if not os.path.exists(apprepo_share) or not os.path.isdir(apprepo_share):
        return content

    path_local = apprepo_share.replace(appdir_root, '')
    content.append('XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:${{APPDIR}}{}'.format(path_local))
    content.append("export XDG_DATA_DIRS=${XDG_DATA_DIRS}\n")

    return content


@factory.apprun(priority=100)
@hexdi.inject('appimage')
def apprun_path_requests_ca_bundle(appdir_root, appimage):
    content = []

    path_debian = "/etc/ssl/certs/ca-certificates.crt"
    content.append("ls {} > /dev/null 2>&1 && REQUESTS_CA_BUNDLE={}".format(path_debian, path_debian))

    path_centos = "/etc/pki/tls/certs/ca-bundle.crt"
    content.append("ls {} > /dev/null 2>&1 && REQUESTS_CA_BUNDLE={}".format(path_centos, path_centos))

    content.append("export REQUESTS_CA_BUNDLE=${REQUESTS_CA_BUNDLE}\n")

    return content


@factory.apprun(priority=110)
@hexdi.inject('appimage')
def apprun_path_gtk2_rc_files(appdir_root, appimage):
    content = []

    apprepo_share = appimage.get_folder_share(appdir_root)
    if not os.path.exists(apprepo_share) or not os.path.isdir(apprepo_share):
        return content

    apprepo_adwaita_gtkrc = "{}/themes/Breeze/gtk-2.0/gtkrc".format(apprepo_share)
    if not os.path.exists(apprepo_adwaita_gtkrc) or not os.path.isfile(apprepo_adwaita_gtkrc):
        return content

    path_local = apprepo_adwaita_gtkrc.replace(appdir_root, '')
    content.append("GTK2_RC_FILES=${{APPDIR}}{}".format(path_local))
    content.append("export GTK2_RC_FILES=${GTK2_RC_FILES}\n")

    return content


@factory.apprun(priority=110)
@hexdi.inject('appimage')
def apprun_path_gst_plugin_path(appdir_root, appimage):
    content = []

    apprepo_lib = appimage.get_folder_lib(appdir_root)
    if not os.path.exists(apprepo_lib) or not os.path.isdir(apprepo_lib):
        return content

    gst_plugin_path = "{}/gstreamer-1.0".format(apprepo_lib)
    if os.path.exists(gst_plugin_path) and os.path.isdir(gst_plugin_path):
        path_local = gst_plugin_path.replace(appdir_root, '')
        content.append("GST_PLUGIN_PATH=${{GST_PLUGIN_PATH}}:${{APPDIR}}{}".format(path_local))

    gst_plugin_path = "{}/gstreamer1.0".format(apprepo_lib)
    if os.path.exists(gst_plugin_path) and os.path.isdir(gst_plugin_path):
        path_local = gst_plugin_path.replace(appdir_root, '')
        content.append("GST_PLUGIN_PATH=${{GST_PLUGIN_PATH}}:${{APPDIR}}{}".format(path_local))

    content.append("export GST_PLUGIN_PATH=${GST_PLUGIN_PATH}\n")

    return content
