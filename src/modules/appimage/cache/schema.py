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
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@hexdi.inject('config')
def create_engine(config=None):
    database = config.get('cache.local', '~/.config/apprepo/local.db')
    database = os.path.expanduser(database)

    from sqlalchemy import create_engine
    return create_engine('sqlite:///{}'.format(database), echo=True)


def create_session():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=create_engine())
    return Session()


class Cache(Base):
    __tablename__ = 'Cache'
    id = Column('id', Integer, primary_key=True)
    token = Column('token', Text, default=None)
    slug = Column('slug', Text, default=None)
    hash = Column('hash', Text, default=None)
    name = Column('name', Text, default=None)
    package = Column('package', Text, default=None)
    file = Column('file', Text, default=None)
    outdated = Column('outdated', Boolean, default=False)
    path = Column('path', Text, default=None)
    icon = Column('icon', Text, default=None)
    alias = Column('alias', Text, default=None)


Base.metadata.create_all(bind=create_engine())
