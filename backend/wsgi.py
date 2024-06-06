# -*- coding: utf-8 -*-
""" Web Server Gateway Interface  """

import os
import sys

from flask_socketio import SocketIO
print(sys.path)


from backend.app import create_app

# create and load `.env` file here from the respective environment to overwrite the env settings
# before server is created.

application = create_app (os.getenv('FLASK_CONFIG') or 'default')