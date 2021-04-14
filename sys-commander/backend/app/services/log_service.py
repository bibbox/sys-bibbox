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


    def select(self, activity_id, limit=None):
        pass

        ## TODO:
        # SELECT "id" FROM "Activities" WHERE "name" LIKE '%instance_name%' AND "name" NOT LIKE '%Delete%' ORDER BY "id" DESC LIMIT 1
        # --> do we allow duplicate InstanceNames when original instance is deleted already?
        # 
        # SELECT * FROM "Logs" WHERE "activity_id" = 'activity_id'

