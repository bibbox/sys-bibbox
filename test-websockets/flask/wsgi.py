import flask
from api import app as application, socketio

if __name__ == '__main__':
    # uwsgi does not come here
    socketio.run(application)