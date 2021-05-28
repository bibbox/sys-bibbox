from flask.ctx import RequestContext
from backend import app
from flask_socketio import SocketIO, emit
from backend.app import socketio as sio
import time

socketio = sio


class SocketIOService():
    def __init__(self):
        pass
        #self.socketio = socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

@socketio.on('connect')#, namespace='/socket.io')
def test_connect():
    print('#'*50, ' connected websocket ', '#'*50)
    emit('connected', {'data': 'Connected'}, broadcast=False)#, namespace="/socket.io") # this should only emit event to connected client
    socketio.sleep(0) # when using gevent, socketio.sleep(0) after emit will release cpu and let other tasks do their work. https://github.com/miguelgrinberg/Flask-SocketIO/issues/418#issuecomment-283382281

    #emitInstanceRefresh()
    # count = 0
    # while count < 10:
    #     time.sleep(1)
    #     emit('event from loop', {'test':'data'})
    #     count += 1

@socketio.on('disconnect')#, namespace='/socket.io')
def disconnected():
    print('disconnected')

#@socketio.event
def emitInstanceRefresh():
    print('emitting instance refresh info')
    global socketio
    try:
        socketio.emit('new_instance_data', {'data': 'New Instance Data in Backend'}, namespace='/')#, namespace="/socket.io")
        socketio.sleep(0)
    except Exception as ex:
        print(ex)


@socketio.on('emit_new_instance_data')
def emitTest():
    emit('new_instance_data')
    socketio.sleep(0)

#callback=ack only when emitting to a single client
def ack():
    print('message was received by client')