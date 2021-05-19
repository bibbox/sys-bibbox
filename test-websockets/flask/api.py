from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True) #, engineio_logger=True) 

counter_client = 0
counter_broadcast = 0


@app.route("/")
def hello():
    return f"Hello World! {counter_client} {counter_broadcast}"

@socketio.on('connect')
def test_connect():
    print('new connection')
    #socketio.emit('my response', {'data': 'Connected'})

@socketio.on('connected success')
def connection_success(data):
    print(str(data))

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('custom event')
def test_message(message):
    print('received event' + message)
    #counter_client += 1
    
    global counter_client
    counter_client += 1
    data = {
        'message'   : 'client message: ' + message,
        'type'      : 'client',
        'counter'   : counter_client
    }
    emit('response', data, broadcast=False, callback=message_received)

@socketio.on('custom broadcast event')
def test_message(message):
    print('received event' + message)
    #counter_client += 1
    
    global counter_broadcast
    counter_broadcast += 1
    data = {
        'message'   : 'broadcast message: ' + message,
        'type'      : 'client',
        'counter'   : counter_broadcast
    }
    socketio.emit('response', data, broadcast=True, callback=message_received)

def message_received(methods=['GET', 'POST']):
    print('message was received')


if __name__ == '__main__':
    socketio.run(app)