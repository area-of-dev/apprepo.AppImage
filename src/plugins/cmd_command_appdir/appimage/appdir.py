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
import shutil
import stat

import hexdi


@hexdi.inject('package.manager')
def get_packages(packages=[], arch='x86_64,noarch', package_manager=None):
    return package_manager.get_packages(packages, arch)


@hexdi.inject('package.manager')
def download(package=None, destination=None, package_manager=None):
    return package_manager.download(package, destination)


@hexdi.inject('package.manager')
def unpack(package=None, destination=None, package_manager=None):
    return package_manager.unpack(package, destination)


def simplify(appdir_root, appdir_build):
    apprepo_bin = '{}/bin'.format(appdir_root)
    apprepo_share = '{}/share'.format(appdir_root)
    apprepo_libexec = '{}/libexec'.format(appdir_root)
    apprepo_lib = '{}/lib'.format(appdir_root)

    copypool = []

    copypool.append(('{}/usr/sbin/*'.format(appdir_build), apprepo_bin))
    copypool.append(('{}/usr/bin/*'.format(appdir_build), apprepo_bin))
    copypool.append(('{}/bin/*'.format(appdir_build), apprepo_bin))

    copypool.append(('{}/usr/lib/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/usr/lib64/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/lib64/*'.format(appdir_build), apprepo_lib))
    copypool.append(('{}/lib/*'.format(appdir_build), apprepo_lib))

    copypool.append(('{}/lib/libexec/*'.format(appdir_build), apprepo_libexec))

    copypool.append(('{}/usr/share/*'.format(appdir_build), apprepo_share))
    copypool.append(('{}/share/*'.format(appdir_build), apprepo_share))
    copypool.append(('{}/share/applications/*.desktop'.format(appdir_root), appdir_root))

    copypool.append(('{}/x86_64-linux-gnu/*'.format(apprepo_lib), apprepo_lib))
    copypool.append(('{}/libexec/*'.format(apprepo_lib), apprepo_libexec))

    for source, destination in copypool:
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)

        os.system("cp --recursive --force {} {}".format(source, destination))
        os.system("rm -rf {}".format(source.strip('/*')))

        yield source, destination

    command = []
    command.append("export XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:{}".format(apprepo_share))
    command.append("export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:{}".format(apprepo_lib))
    command.append("{}/glib-2.0/glib-compile-schemas {}/glib-2.0/schemas/ > /dev/null 2>&1".format(apprepo_lib, apprepo_share))
    command.append("{}/glib-compile-schemas {}/glib-2.0/schemas/ > /dev/null 2>&1".format(apprepo_bin, apprepo_share))
    os.system(" && ".join(command))


    command = []
    command.append("export XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:{}".format(apprepo_share))
    command.append("export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:{}".format(apprepo_lib))
    command.append("{}/update-mime-database {}/mime".format(apprepo_bin, apprepo_share))
    os.system(" && ".join(command))

    GDK_PIXBUF_MODULEDIR = "{}/gdk-pixbuf-2.0/2.10.0/loaders".format(apprepo_lib)
    GDK_PIXBUF_MODULE_FILE = "{}/gdk-pixbuf-2.0/2.10.0/loaders.cache".format(apprepo_lib)

    if os.path.exists(GDK_PIXBUF_MODULEDIR) and os.path.isdir(GDK_PIXBUF_MODULEDIR):
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

    shutil.rmtree(appdir_build, ignore_errors=True)


def _get_folders(enterpoint):
    pool = [enterpoint]

    while len(pool):
        location = pool.pop()
        yield location
        for path in glob.glob("{}**/*".format(location), recursive=True):
            if os.path.isfile(path):
                continue
            if path.find('__pycache__') == -1:
                pool.append(path)


def apprun(appdir_root):
    apprepo_bin = '{}/bin'.format(appdir_root)
    apprepo_share = '{}/share'.format(appdir_root)
    apprepo_libexec = '{}/libexec'.format(appdir_root)
    apprepo_lib = '{}/lib'.format(appdir_root)
    apprepo_libqt5 = '{}/lib/qt5'.format(appdir_root)
    apprepo_libgi = '{}/lib/python'.format(appdir_root)

    content = ["""#! /bin/bash    
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
    """]

    content.append("#APPDIR=`pwd`\n\n")

    if os.path.exists(apprepo_bin) and os.path.isdir(apprepo_bin):
        for path in _get_folders(apprepo_bin):
            path_local = path.replace(appdir_root, '')
            content.append('PATH=${{PATH}}:${{APPDIR}}{}'.format(path_local))

    if os.path.exists(apprepo_libexec) and os.path.isdir(apprepo_libexec):
        for path in _get_folders(apprepo_libexec):
            path_local = path.replace(appdir_root, '')
            content.append('PATH=${{PATH}}:${{APPDIR}}{}'.format(path_local))
        content.append("export PATH=${PATH}\n")

    if os.path.exists(apprepo_lib) and os.path.isdir(apprepo_lib):
        path_local = apprepo_lib.replace(appdir_root, '')

        content.append('GDK_PIXBUF_MODULEDIR=${{APPDIR}}{}/gdk-pixbuf-2.0/2.10.0/loaders'.format(path_local))
        content.append("export GDK_PIXBUF_MODULEDIR=${GDK_PIXBUF_MODULEDIR}\n")

        content.append('GDK_PIXBUF_MODULE_FILE=${{APPDIR}}{}/gdk-pixbuf-2.0/2.10.0/loaders.cache'.format(path_local))
        content.append("export GDK_PIXBUF_MODULE_FILE=${GDK_PIXBUF_MODULE_FILE}\n")

        content.append('GTK_PATH=${{APPDIR}}{}/gtk-2.0'.format(path_local))
        content.append("export GTK_PATH=${GTK_PATH}\n")

        content.append('GTK_IM_MODULE_FILE=${{APPDIR}}{}/gtk-2.0'.format(path_local))
        content.append("export GTK_IM_MODULE_FILE=${GTK_IM_MODULE_FILE}\n")

        content.append('PANGO_LIBDIR=${{APPDIR}}{}'.format(path_local))
        content.append("export PANGO_LIBDIR=${PANGO_LIBDIR}\n")

        for path in _get_folders(apprepo_lib):
            path_local = path.replace(appdir_root, '')
            content.append('LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:${{APPDIR}}{}'.format(path_local))
        content.append('LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:${{APPDIR}}{}/gdk-pixbuf-2.0/loaders'.format(path_local))
        content.append("export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}\n")

    if os.path.exists(apprepo_libgi) and os.path.isdir(apprepo_libgi):
        for path in _get_folders(apprepo_libgi):
            path_local = path.replace(appdir_root, '')
            content.append('GI_TYPELIB_PATH=${{GI_TYPELIB_PATH}}:${{APPDIR}}{}'.format(path_local))
        content.append("export GI_TYPELIB_PATH=${GI_TYPELIB_PATH}\n")

    if os.path.exists(apprepo_libqt5) and os.path.isdir(apprepo_libqt5):
        for path in _get_folders(apprepo_libqt5):
            path_local = path.replace(appdir_root, '')
            content.append('QT_PLUGIN_PATH=${{QT_PLUGIN_PATH}}:${{APPDIR}}{}'.format(path_local))
        content.append("export QT_PLUGIN_PATH=${QT_PLUGIN_PATH}\n")

    apprepo_libperl = '{}/lib/perl5'.format(appdir_root)
    if os.path.exists(apprepo_libperl) and os.path.isdir(apprepo_libperl):
        for path in _get_folders(apprepo_libperl):
            path_local = path.replace(appdir_root, '')
            content.append('PERL5LIB=${{PERL5LIB}}:${{APPDIR}}{}'.format(path_local))
        content.append("export PERL5LIB=${PERL5LIB}\n")

    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.6')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.6/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.6/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.6/lib-dynload')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.8')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.8/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.8/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.8/lib-dynload')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.9')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.9/site-packages')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.9/site-packages/PIL')
    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/lib/python3.9/lib-dynload')

    content.append('PYTHONPATH=${PYTHONPATH}:${APPDIR}/vendor')
    content.append("export PYTHONPATH=${PYTHONPATH}\n")

    if os.path.exists(apprepo_share) and os.path.isdir(apprepo_share):
        path_local = apprepo_share.replace(appdir_root, '')
        content.append('XDG_DATA_DIRS=${{XDG_DATA_DIRS}}:${{APPDIR}}{}'.format(path_local))
        content.append("export XDG_DATA_DIRS=${XDG_DATA_DIRS}\n")

    content.append("ls /etc/ssl/certs/ca-certificates.crt > /dev/null 2>&1 && REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt\n")
    content.append("ls /etc/pki/tls/certs/ca-bundle.crt  > /dev/null 2>&1 && REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt\n")
    content.append("export REQUESTS_CA_BUNDLE=${REQUESTS_CA_BUNDLE}\n")

    content.append("#exec ${APPDIR}/bin/....\n")

    apprun = "{}/AppRun".format(appdir_root)
    with open(apprun, "w") as stream:
        stream.write("\n".join(content))
        stream.close()

        os.chmod(apprun, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    yield "\n".join(content)
