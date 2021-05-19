from backend import app
from flask_socketio import SocketIO, emit
from backend.app import socketio

#socketio = SocketIO(cors_allowed_origins="*", logger=True)

class SocketIOService():
    def __init__(self):
        pass

    @socketio.on('connect')
    def test_connect():
        emit('my response', {'data': 'Connected'})

    @socketio.on('disconnect', namespace='/socket.io')
    def disconnected(message):
        print('disconnected')

    @socketio.event
    def emitInstanceRefresh():
        socketio.emit('new instance data', broadcast=True)