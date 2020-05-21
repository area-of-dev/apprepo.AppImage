import os
import pty
import subprocess
import configparser
from multiprocessing.pool import ThreadPool
import glob


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
        desktop_wanted = os.path.basename(desktop_origin)
        desktop_wanted = "{}/{}".format(destination, desktop_wanted)
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
        appimage = os.path.basename(self.appimage)
        appimage = appimage.replace('.AppImage', '')

        icon_origin = self._icon_origin()
        icon_origin = os.path.basename(icon_origin)
        icon_origin = icon_origin.split('.')

        icon_origin[0] = appimage
        return '.'.join(icon_origin)

    def property(self, origin=None):
        origin = os.path.basename(self.appimage)
        return origin.replace('.AppImage', '')

    def files(self, destination=None):
        icon_origin = self._icon_origin()
        icon_wanted = self._icon_wanted()
        icon_wanted = "{}/{}".format(destination, icon_wanted)
        return (icon_origin, icon_wanted)


def appimage_integration(appimage, prefix='/usr/share'):
    out_r, out_w = pty.openpty()
    process = subprocess.Popen([appimage, '--appimage-mount'], stdout=out_w, stderr=subprocess.PIPE)
    path_mounted = str(os.read(out_r, 1024), 'utf-8', errors='ignore')
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

    property_exec = config.get('Desktop Entry', 'Exec')
    config.set('Desktop Entry', 'Exec', desktopfinder.property(property_exec))

    property_icon = config.get('Desktop Entry', 'Icon')
    config.set('Desktop Entry', 'Icon', iconfinder.property(property_icon))

    with open(desktop_wanted, 'w') as desktop_wanted_stream:
        config.write(desktop_wanted_stream)

    with open(icon_origin, 'rb') as icon_origin_stream:
        with open(icon_wanted, 'wb') as icon_wanted_stream:
            icon_wanted_stream.write(icon_origin_stream.read())

    process.terminate()

    return (desktop_wanted, icon_wanted)


pool = ThreadPool(processes=1)

# appimage = '/home/sensey/Applications/Krita.AppImage'
appimage = '/home/sensey/Applications/Audacity.AppImage'
appimage = '/home/sensey/Applications/AOD-Notes.AppImage'
async_result = pool.apply_async(appimage_integration, (appimage, '{}/.local/share'.format(os.path.expanduser('~'))))
print(async_result.get())
