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


class Activity (BaseModel, db.Model):
    """Model for Activity table"""
    __tablename__ = "Activities"

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128), nullable=False)
    type_           = db.Column(db.String(20), nullable=False)
    start_time      = db.Column(db.DateTime, nullable=False)
    finished_time   = db.Column(db.DateTime, nullable=True)
    state           = db.Column(db.String, nullable=False)
    result          = db.Column(db.String, nullable=True)

    logs            = db.relationship(
                        'Log', 
                        back_populates='activity', 
                        lazy=True, 
                        cascade="all, delete",
                        passive_deletes=False)

    def __init__(self, name, type_, start_time, finished_time, state, result):
        super().__init__()
        self.name           = name
        self.type_          = type_
        self.start_time     = start_time
        self.finished_time  = finished_time
        self.state          = state
        self.result         = result



'''
    removed: user_id, user_name --> unnecessary


  {
    "name": "Name of the activity, specified by the owner of the task",
    "type": "INSTALLAPP | UPDATEAPP | DELETEAPP | BACKUPAPP",
    "user_id": 8776,
    "user_name": "Name of the user issued the task / job", 
    "start_time" : "start time in javascript format",  
    "finished_time":  "finished time in javascript format, empty string when still running",
    "state" : "RUNNING | FINISHED | PAUSED",
    "result" : "SUCCESS | ERROR | UNKNOWN"
  }
'''