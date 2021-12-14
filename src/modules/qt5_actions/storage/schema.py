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
from datetime import datetime

import hexdi
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@hexdi.inject('config')
def create_engine(config=None):
    database = config.get('actions.storage', '~/.config/apprepo/actions.db')
    database = os.path.expanduser(database)

    from sqlalchemy import create_engine
    return create_engine('sqlite:///{}'.format(database), connect_args={
        'check_same_thread': False
    }, echo=True)


def create_session():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=create_engine(), autocommit=True)
    return Session()


class Action(Base):
    __tablename__ = 'Action'

    id = Column('id', sqlalchemy.Integer, primary_key=True)
    action = Column('action', sqlalchemy.Text, default=None)
    appimage = Column('appimage', sqlalchemy.Text, default=None)
    package = Column('package', sqlalchemy.JSON, default=None)

    progress = Column('progress', sqlalchemy.Integer, default=None)

    created_at = Column('created_at', sqlalchemy.DateTime, default=datetime.now)
    finished_at = Column('finished_at', sqlalchemy.DateTime, default=None)


Base.metadata.create_all(bind=create_engine())
