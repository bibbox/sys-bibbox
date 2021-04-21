# -*- coding: utf-8 -*-

from flask import Flask

from sqlalchemy import inspect

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

    # def _as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # Preferred way
    # https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(BaseModel, db.Model):
    """Model for users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    # using func.now(), so time is calculated by the DB server and not by server backend.
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    created_date = db.Column(db.DateTime, nullable=False, default=func.now())

    def __init__(self, username, email="", password_hash=""):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user