import logging
import os
from logging.handlers import RotatingFileHandler

from backend.app.models.log import Log
from backend.app import db


# A very basic logger-handler that commits a LogRecord to the SQL Db
class DBLogsHandler(logging.Handler):
    def __init__(self, activity_id):
        super(DBLogsHandler, self).__init__()
        self.activity_id = activity_id

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        
        log = Log(
            timestamp   = record.__dict__['asctime'],
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
        MAX_BYTES = 5000000 # Maximum size for a log file
        BACKUP_COUNT = 3 # Maximum number of old log files
        
        # TODO: Move to /var/log/bibbox/
        # - mount folder into bibbox-sys-commander-backend container

        log_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')

        debug_file_handler = RotatingFileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../logs/debug.log'), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        debug_file_handler.setFormatter(log_format)
        debug_file_handler.setLevel(logging.DEBUG)

        info_file_handler = RotatingFileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)),  '../../logs/info.log'), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        info_file_handler.setFormatter(log_format)
        info_file_handler.setLevel(logging.INFO)

        warn_file_handler = RotatingFileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)),  '../../logs/warning.log'), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        warn_file_handler.setFormatter(log_format)
        warn_file_handler.setLevel(logging.WARNING)
        
        error_file_handler = RotatingFileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../logs/error.log'), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        error_file_handler.setFormatter(log_format)
        error_file_handler.setLevel(logging.ERROR)

        db_handler = DBLogsHandler(self.activity_id)
        db_handler.setLevel(logging.INFO)

        logger = logging.getLogger(self.logger_name)
        logger.addHandler(debug_file_handler)
        logger.addHandler(info_file_handler)
        logger.addHandler(warn_file_handler)
        logger.addHandler(error_file_handler)
        logger.addHandler(db_handler)

        return logger