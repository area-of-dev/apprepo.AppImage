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
import hexdi


class PackageManagerFactory(object):

    @hexdi.inject('config')
    def is_excluded(self, package, config):
        excludes = [
            'X11', 'x11', 'xorg', 'xserver-xorg-core', 'xserver-common', 'xserver-xorg-legacy',
            'glibc', 'clib', 'libgcc', 'libc6',
            'debianutils',
            'centos',
            'setup',
            'bash',
            'mesa',
            'basesystem',
            'systemd',
            'filesystem',
            'dbus',
            'coreutils',
            'shadow-utils',
            'systemd-pam', 'systemd-udev',
            'fuse',
            'pkgconf',
            'xorg-x11-server-utils',
            'adwaita-cursor-theme',
            'xkeyboard-config',
            'wayland',
            'ca-certificates',
            'iso-codes',
            'zenity',
            'udisks2',
            'device-mapper',
            'mdadm',
            'util-linux',
            'chkconfig',
            'sed',
            'gawk',
            'which',
            'desktop-file-utils',
            'adduser',
            'apparmor',
            'automake',
            'autoconf',
            'autotools',
            # 'file',
            'dpkg',
            'gcc',
            'linux',
            'nvidia',
            'avahi',
            'cups',
            'login',
            'shadow',
            'patch',
            'clang',
            'acpid',
            'dkms',
            'make',
            'dconf',
            'debconf',
            'init-system-helpers',
            'sensible-utils',
            'passwd',
            'usermod',
            'userdel',
            'mount',
            'ucf',
            'cpp', 'g++',
            'udev',
            'glib-networking', 'glib-networking-common', 'glib-networking-services',
        ]

        for pattern in excludes:
            if package.name.find(pattern) == 0:
                return True
        return False

    def _get_package_manager(self):
        try:
            from . import apt
            return apt
        except ImportError as ex:
            pass

        # try:
        #     from . import dnf
        #     return dnf
        # except ImportError as ex:
        #     pass

        raise Exception('No package manager available')

    def get_packages(self, packages=[], arch='amd64,x86_64,noarch'):
        package_manager = self._get_package_manager()
        if not package_manager: raise Exception('Package manager not available')

        pool = []

        for package in package_manager.get_packages(packages, arch):
            if package in pool:
                continue

            if self.is_excluded(package):
                continue

            pool.append(package)

        return pool

    def download(self, package=None, destination=None):
        package_manager = self._get_package_manager()
        if not package_manager: raise Exception('Package manager not available')

        return package_manager.download(package, destination)

    def unpack(self, package=None, destination=None):
        package_manager = self._get_package_manager()
        if not package_manager: raise Exception('Package manager not available')

        return package_manager.unpack(package, destination)
