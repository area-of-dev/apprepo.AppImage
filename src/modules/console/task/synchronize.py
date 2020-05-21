import os
import sys
import pty
import pathlib
import subprocess
import configparser
from multiprocessing.pool import ThreadPool
import glob
import optparse
import inject


class EqualsSpaceRemover(object):
    def __init__(self, origin):
        self.origin = origin

    def write(self, what):
        self.origin.write(what.replace(" = ", "=", 1))


class AppImageDesktopFinder(object):
    def __init__(self, appimage, mountpoint):
        self.mountpoint = mountpoint
        self.appimage = appimage

    def _desktop_origin(self):
        pattern = '{}/*.desktop'.format(self.mountpoint)
        for path in glob.glob(pattern):
            return path

    def property(self, origin=None):
        properties = origin.split(' ')
        properties[0] = self.appimage
        return ' '.join(properties)

    def files(self, destination=None):
        desktop_origin = self._desktop_origin()

        desktop_wanted = pathlib.Path(self.appimage)
        desktop_wanted = desktop_wanted.stem
        desktop_wanted = "{}/{}.desktop".format(destination, desktop_wanted)
        return (desktop_origin, desktop_wanted)


class AppImageIconFinder(object):
    def __init__(self, appimage, mountpoint):
        self.mountpoint = mountpoint
        self.appimage = appimage

    def _icon_origin(self):
        pattern = '{}/*.svg'.format(self.mountpoint)
        for path_temp_icon in glob.glob(pattern):
            return path_temp_icon

        pattern = '{}/*.png'.format(self.mountpoint)
        for path_temp_icon in glob.glob(pattern):
            return path_temp_icon

        pattern = '{}/*.jpg'.format(self.mountpoint)
        for path_temp_icon in glob.glob(pattern):
            return path_temp_icon

        pattern = '{}/*.ico'.format(self.mountpoint)
        for path_temp_icon in glob.glob(pattern):
            return path_temp_icon

        return None

    def _icon_wanted(self):
        appimage = pathlib.Path(self.appimage)
        appimage = appimage.stem

        icon_origin = self._icon_origin()
        icon_origin = pathlib.PurePosixPath(icon_origin)
        return ''.join([appimage, icon_origin.suffix])

    def property(self, origin=None):
        origin = pathlib.Path(self.appimage)
        return origin.stem

    def files(self, destination=None):
        icon_origin = self._icon_origin()
        icon_wanted = self._icon_wanted()
        icon_wanted = "{}/{}".format(destination, icon_wanted)
        return (icon_origin, icon_wanted)


def appimage_integration(appimage, prefix='/usr/share'):
    out_r, out_w = pty.openpty()
    process = subprocess.Popen([appimage, '--appimage-mount'], stdout=out_w, stderr=subprocess.PIPE)
    path_mounted = str(os.read(out_r, 2048), 'utf-8', errors='ignore')
    path_mounted = path_mounted.strip("\n\r")

    path_desktop = '{}/applications'.format(prefix)
    os.makedirs(path_desktop, exist_ok=True)

    path_icon = '{}/icons'.format(prefix)
    os.makedirs(path_icon, exist_ok=True)

    desktopfinder = AppImageDesktopFinder(appimage, path_mounted)
    desktop_origin, desktop_wanted = desktopfinder.files(path_desktop)

    iconfinder = AppImageIconFinder(appimage, path_mounted)
    icon_origin, icon_wanted = iconfinder.files(path_icon)

    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(desktop_origin)

    if not config.has_option('Desktop Entry', 'Version'):
        config.set('Desktop Entry', 'Version', 1.0)

    property_icon = config.get('Desktop Entry', 'Icon')
    config.set('Desktop Entry', 'Icon', iconfinder.property(property_icon))

    for section in config.sections():
        if config.has_option(section, 'Exec'):
            property_exec = config.get(section, 'Exec')
            config.set(section, 'Exec', desktopfinder.property(property_exec))

        if config.has_option(section, 'TryExec'):
            property_exec = config.get(section, 'TryExec')
            config.set(section, 'TryExec', desktopfinder.property(property_exec))

    with open(desktop_wanted, 'w') as desktop_wanted_stream:
        config.write(EqualsSpaceRemover(desktop_wanted_stream))

    with open(icon_origin, 'rb') as icon_origin_stream:
        with open(icon_wanted, 'wb') as icon_wanted_stream:
            icon_wanted_stream.write(icon_origin_stream.read())
            icon_wanted_stream.close()
        icon_origin_stream.close()

    process.terminate()

    return (desktop_wanted, icon_wanted)


@inject.params(config='config', logger='logger')
def main(options=None, args=None, config=None, logger=None):
    pool = ThreadPool(processes=1)

    applications_global = config.get('applications.global', '/Applications')
    applications_global = applications_global.split(':')

    applications_local = config.get('applications.local', '~/Applications')
    applications_local = applications_local.split(':')

    integration = '/usr/share' \
        if options.systemwide else \
        os.path.expanduser('~/.local/share')

    applications = applications_global \
        if options.systemwide else \
        applications_local

    for location in applications:
        location = os.path.expanduser(location)
        if location is None: continue

        for appimage in glob.glob('{}/*.AppImage'.format(location)):
            yield "Application: {}".format(appimage)
            async_result = pool.apply_async(appimage_integration, (appimage, integration))
            desktop, icon = async_result.get()
            yield "\tupdating desktop file: {}".format(desktop)
            yield "\tupdating desktop icon file: {}".format(icon)

    return 0
