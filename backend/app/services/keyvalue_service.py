# -*- coding: utf-8 -*-
"""

CatalogueService class - This class holds the method related to User manipulations.

"""
from sqlalchemy import *

from backend.app.models.app import db
from backend.app.models.keyvalue import KeyValue
from backend.app.services import SQLAlchemyService


class KeyValueService(SQLAlchemyService):
    __model__ = KeyValue

    def __init__(self):
        self.parentClassRef = super(KeyValueService, self)

    def get_value_by_key (self, search_key):
        c = self.__model__.query.filter(self.__model__.keys == search_key ).first()
        return c

