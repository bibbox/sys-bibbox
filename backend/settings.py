# -*- coding: utf-8 -*-
"""
    file: settings.py
    notes:  Configure Settings for application
"""
import os

from dotenv import load_dotenv
load_dotenv()



class Config(object):
    """ Common config options """

    APPNAME = 'BIBBOX COMMANDER'
    SUPPORT_EMAIL = 'heimo.mueller@mac.com'
    VERSION = '0.0.1'
    APPID = 'bibbox-commander'
    SECRET_KEY = os.urandom(24)
    TESTING = False

    SSE_REDIS_URL = 'redis://redis:6379'

    SECRET_KEY = 'the quick brown fox jumps over the lazy dog'

    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASS = os.getenv('POSTGRES_PASSWORD')
    DB_SERVICE = os.getenv('DB_SERVICE')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_NATIVE_UNICODE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME)

    print ("I'm in DEFAULT config", SQLALCHEMY_DATABASE_URI)

    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


class DevelopmentConfig(Config):
    """ Dev environment config options """
    FLASK_ENV='development'
    DEBUG = True
    PROFILE = True

class DevelopmentConfigLocal(Config):
    """ Dev environment config options for local python developent"""
    FLASK_ENV='development'

    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASS = os.getenv('POSTGRES_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_SERVICE = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME)

    print ("I'm in DEV LOCAL config", SQLALCHEMY_DATABASE_URI)

    CELERY_BROKER_URL = '127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = '127.0.0.1:6379/0'
    SSE_REDIS_URL = '127.0.0.1:6379'

    DEBUG = True
    PROFILE = True

class TestingConfig(Config):
    """ Testing environment config options """
    DEBUG = False
    STAGING = True
    TESTING = True


class ProductionConfig(Config):
    """ Prod environment config options """
    FLASK_ENV = 'production'
    DEBUG = False
    STAGING = False


config = {
    'development':      DevelopmentConfig,
    'developmentlocal': DevelopmentConfigLocal,
    'testing':          TestingConfig,
    'production':       ProductionConfig,
    'default':          DevelopmentConfig
}

