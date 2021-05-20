from backend import app
from flask_socketio import SocketIO, emit
from backend.app import socketio


class SocketIOService():
    def __init__(self):
        self.socketio = socketio #needed?

    @socketio.on('connect')#, namespace='/socket.io')
    def test_connect():
        print('#'*50, ' connected websocket ', '#'*50)
        emit('connected', {'data': 'Connected'})#, namespace="/socket.io") # this should only emit event to connected client
        socketio.sleep(0) # when using gevent, socketio.sleep(0) after emit will release cpu and let other tasks do their work. https://github.com/miguelgrinberg/Flask-SocketIO/issues/418#issuecomment-283382281

    @socketio.on('disconnect')#, namespace='/socket.io')
    def disconnected():
        print('disconnected')

    @socketio.event
    def emitInstanceRefresh():
        print('emitting instance refresh info')
        try:
            socketio.emit('new_instance_data', {'data': 'New Instance Data in Backend'}, namespace='/')#, namespace="/socket.io")
            socketio.sleep(0)
        except Exception as ex:
            print(ex)