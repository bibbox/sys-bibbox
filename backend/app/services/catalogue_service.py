# -*- coding: utf-8 -*-
"""

CatalogueService class - This class holds the method related to User manipulations.

"""

from backend.app.models.catalogue import Catalogue
from backend.app.services import SQLAlchemyService


class CatalogueService(SQLAlchemyService):
    __model__ = Catalogue

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(CatalogueService, self)

    def catalogue (self, catalogueName):
        
        c = self.__model__.query.filter(self.__model__.name.in_([catalogueName])).first()
        return c


