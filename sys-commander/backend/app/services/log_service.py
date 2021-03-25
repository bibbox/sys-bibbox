# -*- coding: utf-8 -*-
"""

LogService class - This class holds the method related to Log manipulations.

"""

from backend.app.models.log import Log
from backend.app.services import SQLAlchemyService


class LogService(SQLAlchemyService):
    __model__ = Log

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(LogService, self)

