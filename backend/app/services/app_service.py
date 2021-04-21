# -*- coding: utf-8 -*-
"""

CatalogueService class - This class holds the method related to User manipulations.

"""
from sqlalchemy import *

from backend.app.models.app import BibboxApp
from backend.app.services import SQLAlchemyService


class AppService(SQLAlchemyService):
    __model__ = BibboxApp

    def __init__(self):
        self.parentClassRef = super(AppService, self)

    def version (self, appid, version):      
        c = self.__model__.query.filter(and_ (self.__model__.appid == appid ,
                                              self.__model__.version == version)).first()
        return c

