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
import os

import hexdi
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

session = None


@hexdi.inject('config')
def create_engine(config=None):
    database = config.get('cache.global', '~/.config/apprepo/remote.db')
    database = os.path.expanduser(database)

    from sqlalchemy import create_engine
    return create_engine('sqlite:///{}'.format(database), connect_args={
        'check_same_thread': False
    }, echo=True)


def create_session():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=create_engine())
    return Session()


GroupPackageMapping = Table('GroupPackageMapping', Base.metadata,
                            Column('groupId', Integer, ForeignKey('PackageGroup.id')),
                            Column('packageId', Integer, ForeignKey('Package.id'))
                            )


class PackageGroup(Base):
    __tablename__ = 'PackageGroup'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text, default=None)
    description = Column('description', Text, default=None)
    icon = Column('icon', Text, default=None)

    packages = relationship("Package", secondary=GroupPackageMapping, back_populates="groups")


class PackageImage(Base):
    __tablename__ = 'PackageImage'

    id = Column('id', Integer, primary_key=True)
    url = Column('url', Text, default=None)

    package_id = Column(Integer, ForeignKey('Package.id'))
    package = relationship("Package", back_populates="images")


class Package(Base):
    __tablename__ = 'Package'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text, default=None)
    package = Column('package', Text, default=None)
    slug = Column('slug', Text, default=None)
    token = Column('token', Text, default=None)
    version = Column('version', Text, default=None)
    description = Column('description', Text, default=None)
    hash = Column('hash', Text, default=None)
    file = Column('file', Text, default=None)

    groups = relationship("PackageGroup", secondary=GroupPackageMapping, back_populates="packages")
    images = relationship("PackageImage", back_populates="package")

    @property
    def image(self):
        for entity in self.images:
            return entity


Base.metadata.create_all(bind=create_engine())
