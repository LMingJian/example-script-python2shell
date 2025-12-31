import eventlet
import socketio
from eventlet import wsgi

sio = socketio.Server()


@sio.event
def connect(sid, environ):
    if environ:
        print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def message(sid, data):
    print('message received with ', data, sid)
    sio.send({'response': 'OK'})


def message_handler(sid, msg):
    print('Received message: ', msg, sid)
    sio.send('OK')


sio.on('user', message_handler)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
wsgi.server(eventlet.listen(('', 5000)), app)
