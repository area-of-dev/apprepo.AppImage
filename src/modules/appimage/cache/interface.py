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



class AppImageCache(object):
    _connection = None

    @hexdi.inject('config')
    def __init__(self, config=None):
        pass

    def count(self):
        from .schema import Cache
        from .schema import create_session

        session = create_session()
        return session.query(Cache).count()

    def collection(self):
        from modules.appimage.apprepo.model import appimage
        from .schema import Cache
        from .schema import create_session

        session = create_session()

        for entity in session.query(Cache).all():
            yield appimage.AppImage(entity.path, entity.slug, entity.outdated)

    def has(self, appimage=None):
        from .schema import Cache
        from .schema import create_session

        if not appimage:
            return None

        session = create_session()

        return session.query(Cache).filter(
            Cache.package == appimage.package
        ).count()

    def add(self, appimage=None):
        from .schema import Cache
        from .schema import create_session

        if not appimage:
            return None

        session = create_session()

        session.add(Cache(
            package=appimage.package,
            hash=appimage.hash,
            path=appimage.path,
            icon=appimage.icon,
            alias=appimage.alias,
        ))

        session.commit()

        return True

    def update(self, appimage=None, info=None):
        from .schema import Cache
        from .schema import create_session

        if not appimage:
            return None

        session = create_session()

        entity: Cache = session.query(Cache).filter(
            Cache.package == appimage.package
        ).first()

        entity.hash = appimage.hash
        entity.path = appimage.path
        entity.icon = appimage.icon
        entity.alias = appimage.alias

        if info and 'name' in info.keys():
            entity.name = info['name']

        if info and 'slug' in info.keys():
            entity.slug = info['slug']

        if info and 'file' in info.keys():
            entity.file = info['file']

        entity.outdated = True
        if appimage.hash == info['hash']:
            entity.outdated = False

        session.commit()
