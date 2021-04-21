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


class BibboxApp (BaseModel, db.Model):
    """Model for App table"""
    __tablename__ = "apps"

    id                      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appid                   = db.Column(db.String(128), nullable=False)
    version                 = db.Column(db.String(128), nullable=False)
    appinfo                 = db.Column(db.UnicodeText(), nullable=False)
    environment_parameters  = db.Column(db.UnicodeText(), nullable=False)

    def __init__(self, appid, version, appinfo, environment_parameters):
        super().__init__()
        self.appid   = appid
        self.version = version
        self.appinfo = appinfo
        self.environment_parameters = environment_parameters