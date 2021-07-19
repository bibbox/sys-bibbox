# -*- coding: utf-8 -*-
"""Angular-Flask-Docker-Skeleton Main application package
"""

# socketio related --> redis needs monkeypatched app, redis is needed for emitting out of context events
# from gevent import monkey
# monkey.patch_all()
# note: monkey patched in uwsgi.ini already

import logging
from re import A
import engineio

from flask import Flask, Blueprint, url_for, render_template
from flask_restplus import Resource, Api
from flask_bootstrap import Bootstrap

from flask_restplus import Resource, Api

from flask_swagger_ui import get_swaggerui_blueprint

from flask_sqlalchemy import SQLAlchemy


from celery import Celery
from celery.signals import after_setup_logger

from backend.settings import config, Config

from flask_cors import CORS
from flask_socketio import SocketIO
# review and restructer tha Application Context
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/ 


bootstrap = Bootstrap()
app = Flask(__name__)

socketio = SocketIO(app, logger=False, engineio_logger=False, cors_allowed_origins="*", namespace='/', message_queue='redis://redis:6379') #, )

db = SQLAlchemy()


apiblueprint = Blueprint('api', __name__)
restapi = Api (apiblueprint)


app_celerey = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_name):
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    print ("CREATE APP IN ", config_name, " MODE")
    
    app.config.from_object(config[config_name])
    # SocketIO.init_app(app=app, cors_allowed_origins="*", logger=True, engineio_logger=True)
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
   
    @app.route("/")
    def main():
        return app.send_static_file('main.html')

    import backend.app.api
    app.register_blueprint(apiblueprint,  url_prefix='/api/v1')



    return app