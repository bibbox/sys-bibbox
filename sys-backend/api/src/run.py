import os

import connexion
import sys
from flask_cors import CORS

sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend/api/src/web")


#from web 
import encoder


def create_app():
    abs_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    openapi_path = os.path.join(abs_file_path, "openapi")
    app = connexion.FlaskApp(
        __name__, specification_dir=openapi_path, options={"swagger_ui": True, "serve_spec": True}
    )
    app.add_api("specification.yml", strict_validation=True)
    flask_app = app.app
    flask_app.config['Access-Control-Allow-Origin'] = '*'
    flask_app.json_encoder = encoder.JSONEncoder
    CORS(flask_app)
    return flask_app

create_app()