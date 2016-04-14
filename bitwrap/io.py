import eventlet
eventlet.monkey_patch()

import logging
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask.ext.cors import CORS


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

q = 'redis://%s:%s' % (
        os.environ['REDIS_PORT_6379_TCP_ADDR'],
        os.environ['REDIS_PORT_6379_TCP_PORT']
    )

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, async_mode='eventlet', message_queue=q)

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@socketio.on('connect', namespace='/chat')
def connect():
    print("connect")

@socketio.on('chat message', namespace='/chat')
def message(msg):
    print("message ", msg)
    socketio.emit('event', msg, namespace='/chat')

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    print('disconnect ')

if __name__ == '__main__':
    socketio.run(app, port=8080, host='0.0.0.0', debug=True)
