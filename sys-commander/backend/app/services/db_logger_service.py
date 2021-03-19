import logging

from backend.app.models.log import Log
from backend.app import db

class DBLogsHandler(logging.Handler):
    def __init__(self, activity_id):
        super(DBLogsHandler, self).__init__()
        self.activity_id = activity_id

    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        
        log = Log(
            log_message = record.__dict__['msg'],
            type_       = record.__dict__['levelname'],
            activity_id = self.activity_id
        )
        db.session.add(log)

        db.session.commit()


class DBLoggerService():
    def __init__(self, activity_id, logger_name):
        self.activity_id = activity_id
        self.logger_name = logger_name
        self.logger = self._configLogger()

    def getLogger(self):
        return self.logger

    def _configLogger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(DBLogsHandler(self.activity_id))
        return logger