# -*- coding: utf-8 -*-
"""Angular-Flask-Docker-Skeleton Main application package
"""


import logging

from flask import Flask
from flask_bootstrap import Bootstrap

from flask_restplus import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

from flask_sqlalchemy import SQLAlchemy

from flask_sse import sse

from celery import Celery
from celery.signals import after_setup_logger

from backend.settings import config, Config

from flask_cors import CORS

#from flask_socketio import SocketIO


# review and restructer tha Application Context
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/ 

bootstrap = Bootstrap()
app = Flask(__name__)
db = SQLAlchemy()

app_celerey = Celery(__name__, broker=Config.CELERY_BROKER_URL)

#socketio = SocketIO()

def create_app(config_name):
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    db.app = app
    app_celerey.conf.update(app.config)

    TaskBase = app_celerey.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    app_celerey.Task = ContextTask

    logger = logging.getLogger(__name__)

    @after_setup_logger.connect
    def setup_loggers(logger, *args, **kwargs):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # SysLogHandler
        slh = logging.handlers.SysLogHandler(address=('logsN.papertrailapp.com', '...'))
        slh.setFormatter(formatter)
        logger.addHandler(slh)

    # swagger base URL has to be specified   
    swaggerui_blueprint = get_swaggerui_blueprint(
        '/bibbox/api/docs',
        '/bibbox/static/bibbox-api-spec.yml',
        config={'app_name': "BIBBOX COMMANDER"}
    )

    app.register_blueprint(swaggerui_blueprint)
    
    from backend.app.api import api as api_1_0_blueprint
    
    app.register_blueprint(api_1_0_blueprint,  url_prefix='/bibbox/api/v1')
    app.register_blueprint(sse, url_prefix='/stream')

#    socketio.init_app(app)
#    return socketio, app

    return app
