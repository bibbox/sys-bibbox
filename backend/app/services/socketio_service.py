from backend import app
from flask_socketio import SocketIO, emit
from backend.app import socketio


class SocketIOService():
    def __init__(self):
        pass

    @socketio.on('connect') #, namespace='/socket.io')
    def test_connect():
        print('#'*50, ' connected websocket ', '#'*50)
        socketio.emit('my response', {'data': 'Connected'}, broadcast=True) #, namespace="/socket.io")
        socketio.sleep(0) # when using gevent, socketio.sleep(0) after emit will release cpu and let other tasks do their work. https://github.com/miguelgrinberg/Flask-SocketIO/issues/418#issuecomment-283382281

    @socketio.on('disconnect') #, namespace='/socket.io')
    def disconnected():
        print('disconnected')

    @socketio.event
    def emitInstanceRefresh():
        print('emitting instance refresh info')
        socketio.emit('new instance data', {'data': 'New Instance Data in Backend'}, broadcast=True) #, namespace="/socket.io")
        socketio.sleep(0)

