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



class AppRepoCache(object):

    def __init__(self):
        self._session = None

    @property
    def session(self):
        from .schema import create_session

        if not self._session:
            self._session = create_session()
        return self._session

    def package_groups(self):
        from .schema import PackageGroup
        for entity in self.session.query(PackageGroup).all():
            yield entity

    def package_group(self, entity):
        from .schema import PackageGroup

        if not entity:
            return None

        return self.session.query(PackageGroup).filter(
            PackageGroup.name == entity['name']
        ).first()

    def has_package_group(self, entity):
        from .schema import PackageGroup

        if not entity:
            return None

        return self.session.query(PackageGroup).filter(
            PackageGroup.name == entity['name']
        ).count()

    def add_package_group(self, entity):
        from .schema import PackageGroup

        if not entity:
            return None

        group = PackageGroup(
            description=entity['description'],
            name=entity['name'],
        )

        self.session.add(group)
        self.session.commit()

        return group

    def clean_package_groups(selfs):
        pass

    def clean_packages(selfs):
        pass

    def packages(self, group = None):
        from .schema import Package

        if group is not None:
            for entity in group.packages:
                yield entity
            return

        for entity in self.session.query(Package).all():
            yield entity

    def package(self, entity):
        from .schema import Package

        if not entity:
            return None

        return self.session.query(Package).filter(
            Package.slug == entity['slug']
        ).first()

    def has_package(self, entity):
        from .schema import Package

        if not entity:
            return None

        return self.session.query(Package).filter(
            Package.slug == entity['slug']
        ).count()

    def add_package(self, entity):
        from .schema import Package

        if not entity:
            return None

        package = Package(
            hash=entity['hash'],
            file=entity['file'],
            version=entity['version'],
            description=entity['description'],
            slug=entity['slug'],
            package=entity['package'],
            name=entity['name'],
        )

        self.session.add(package)
        self.session.commit()

        return package

    def add_package_image(self, entity):
        from .schema import PackageImage

        if not entity:
            return None

        image = PackageImage(
            url=entity['url'],
        )

        self.session.add(image)
        self.session.commit()

        return image
