# -*- coding: utf-8 -*-
"""

LogService class - This class holds the method related to Log manipulations.

"""

from backend.app.models.log import Log
from backend.app.services import SQLAlchemyService
from backend.app import db
import json

class LogService(SQLAlchemyService):
    __model__ = Log

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(LogService, self)


    def selectLogsFromActivity(self, aid, limit=None):
        try:
            logs = list()
            res = db.session.query(Log).filter(Log.activity_id == aid).limit(limit)
            print(res)
            for log in res:
                logs.append({
                    'id'          : log.id,
                    'timestamp'   : log.timestamp,
                    'message'     : log.log_message,
                    'type'        : log.type_,
                    'activity_id' : log.activity_id
                })
            return logs
        except Exception as ex:
            print(ex)