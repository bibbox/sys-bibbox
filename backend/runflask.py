# -*- coding: utf-8 -*-
""" Web Server Gateway Interface  """

import os
import sys
print(sys.path)

from backend.app import create_app
from flask_socketio import SocketIO

app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.app_context.push()
socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
    #pass
