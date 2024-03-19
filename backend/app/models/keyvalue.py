from flask import Flask

from sqlalchemy import inspect, event

from backend.app import db, app
from sqlalchemy.sql import func

from passlib.apps import custom_app_context as pwd_context

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


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

    # Preferred way
    # https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class KeyValue(BaseModel, db.Model):
    """Model for KeyValue table"""
    __tablename__ = "keyvalue"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keys = db.Column(db.String(128), nullable=False, unique=True)
    values = db.Column(db.UnicodeText(), nullable=False)

    def __init__(self, keys, values):
        super().__init__()
        self.keys = keys
        self.values = values


# @event.listens_for(KeyValue.__table__, 'after_create')
# def create_keyvalue(*args, **kwargs):
#     db.session.add(KeyValue(keys='info', values='abc@domain.com'))
#     db.session.add(KeyValue(keys='contact', values='def@domain.com'))
#     db.session.add(KeyValue(keys='imprint', values='def@domain.com'))
#     db.session.add(KeyValue(keys='partners', values='def@domain.com'))
#     db.session.commit()
