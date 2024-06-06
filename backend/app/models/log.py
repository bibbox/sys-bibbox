# -*- coding: utf-8 -*-
from sqlalchemy import inspect

from backend.app import db
from sqlalchemy.sql import func


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self.as_dict().items()
        })

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Log (BaseModel, db.Model):
    """Model for Log table"""
    __tablename__ = "Logs"

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp       = db.Column(db.String, nullable="False")
    log_message     = db.Column(db.String, nullable="False")
    type_           = db.Column(db.String(20), nullable="False")
    activity_id     = db.Column(db.Integer, db.ForeignKey('Activities.id', ondelete="CASCADE"), nullable=False)

    activity        = db.relationship("Activity", back_populates="logs")

    def __init__(self, timestamp, log_message, type_, activity_id):
        super().__init__()
        self.timestamp      = timestamp
        self.log_message    = log_message
        self.type_          = type_
        self.activity_id    = activity_id



'''
  {
    "log-message": "Log Meassage, usaly a multiline string",
    "type" : "INFO | WARNING | ERROR "
  }
'''