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

from modules.cmd import console


@console.task(name=['synchronize', 'sync'],
              description="go through all available AppImage files "
                          "and integrate them into the system if necessary")
@hexdi.inject('appimagetool', 'console.application', 'apprepo', 'appimage.cache', 'apprepo.cache')
def main(options=None, args=None, appimagetool=None, console=None, apprepo=None, cache=None, apprepo_cache=None):
    profile = os.path.expanduser('~/.profile')
    if not os.path.exists(profile) or not os.path.isfile(profile):
        yield "[{}] ~/.profile does not exist, creating...".format(console.blue('notice'))
        with open(profile, 'w+') as stream:
            stream.write('PATH=~/.local/bin:$PATH')
            stream.close()

    apprepo_cache.clean_package_groups()
    for entity in apprepo.groups():
        if not apprepo_cache.has_package_group(entity):
            apprepo_cache.add_package_group(entity)

    apprepo_cache.clean_packages()
    for entity in apprepo.packages():
        if not apprepo_cache.has_package(entity):
            package = apprepo_cache.add_package(entity)
            if not package: continue

            for group in entity['groups']:
                group = apprepo_cache.package_group(group)
                if not group: continue
                package.groups.append(group)

            for image in entity['images']:
                image = apprepo_cache.add_package_image(image)
                if not image: continue
                package.images.append(image)

    return

    yield console.blue("[cache]: synchronizing")
    for appimage in appimagetool.collection():

        try:
            if not cache.has(appimage):
                yield console.green("[cache]: adding, {}".format(appimage))
                cache.add(appimage)

            for entity in apprepo.package(appimage.package):
                cache.update(appimage, entity)
                yield console.blue("[cache]: updating, {}".format(appimage))

        except Exception as ex:
            yield console.error("[cache]: {}, {}".format(
                appimage, ex
            ))

    if not options.synchronize_remote_only:
        yield console.blue("[integration]: synchronizing")
        for appimage in cache.collection():
            alias = appimage.alias
            if not alias: continue

            desktop = appimage.desktop
            if not desktop: continue

            icon = appimage.icon
            if not icon: continue

            if os.path.exists(appimage.desktop) and os.path.exists(appimage.alias) \
                    and os.path.exists(appimage.icon):
                continue

            yield console.comment("[integration]: missed, {}".format(appimage))

            try:
                appimage = appimagetool.integrate(appimage)
                if not appimage: raise ValueError('Integration failed')

                yield console.green("[integration]: {}, {}, {}, {}".format(
                    os.path.basename(appimage.path) if os.path.exists(appimage.path) else "---",
                    os.path.basename(appimage.desktop) if os.path.exists(appimage.desktop) else "---",
                    os.path.basename(appimage.icon) if glob.glob(appimage.icon) else "---",
                    os.path.basename(appimage.alias) if os.path.exists(appimage.alias) else "---",
                ))

            except Exception as ex:
                yield console.error("[error]: {}, {}".format(
                    appimage.path, ex
                ))
