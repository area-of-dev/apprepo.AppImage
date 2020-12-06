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


@hexdi.permanent('package.manager')
class PackageManager(object):
    pass

    def _get_package_manager(self):
        try:
            from .package_manager import dnf
            return dnf
        except ImportError as ex:
            pass

        try:
            from .package_manager import apt
            return apt
        except ImportError as ex:
            pass

        raise Exception('No package manager available')

    @hexdi.inject('config')
    def is_excluded(self, package, config):
        excludes = [
            'X11', 'x11', 'xorg',
            'glibc',
            'centos',
            'setup',
            'bash',
            'mesa',
            'basesystem',
            'systemd',
            'filesystem',
            'dbus', 'dbus-daemon', 'dbus-tools', 'dbus-common',
            'coreutils',
            'shadow-utils',
            'systemd-pam', 'systemd-udev',
            'fuse',
            'pkgconf', 'pkgconf-pkg-config',
            'xorg-x11-server-utils',
            'adwaita-cursor-theme',
            'xkeyboard-config',
            'wayland', 'libwayland-cursor',
            'ca-certificates',
            'iso-codes',
            'zenity',
            'udisks2',
            'parted',
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
            'automake','autoconf','autotools-dev'
            'file',
            'dpkg',
            'gcc', 'gcc-10-base', 'gcc-9', 'gcc-8', 'gcc-7', 'gcc-10',
            'linux','linux-libc-dev',
            'nvidia-graphics-drivers',
            'avahi',
            'cups',
            'login',
            'passwd',
            'patch',
            'clang',
            'acpid',
            'dkms',
            'make',
            'dconf', 'dconf-service',
        ]
        for pattern in excludes:
            if package.name.find(pattern) == 0:
                return True
            continue
        return False

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
