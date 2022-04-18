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
from datetime import datetime

from sqlalchemy import desc, asc

from .schema import Action


class ActionsStorage(object):

    def __init__(self):
        self._session = None

    def instance(self):
        self._session = None
        return self

    @property
    def session(self):
        from .schema import create_session

        if not self._session:
            self._session = create_session()
        return self._session

    def next(self):
        return self.session.query(Action). \
            filter(Action.finished_at.is_(None)). \
            filter(Action.cancelled_at.is_(None)). \
            order_by(desc(Action.id)).first()

    def actions(self):
        collection = self.session.query(Action). \
            filter(Action.finished_at.is_(None)). \
            order_by(asc(Action.finished_at)). \
            all()

        for entity in collection:
            yield entity

    def refresh(self, entity):
        self.session.refresh(entity)
        return entity

    def update(self, entity):
        with self.session.begin():
            self.session.add(entity)
            self.session.commit()
            self.session.flush()
        return entity

    def add_action(self, model):
        if not model: return None

        entity = Action(
            action=model.get('action', None),
            appimage=model.get('appimage', None),
            package=model.get('package', None),
            progress=model.get('progress', 0),
            created_at=datetime.now(),
            processed_at=None,
            cancelled_at=None,
            finished_at=None
        )

        with self.session.begin():
            self.session.add(entity)
            self.session.commit()
            self.session.flush()
        return entity
