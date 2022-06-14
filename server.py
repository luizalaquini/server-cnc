import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
    '/css/style.css': 'css/style.css'
})

@sio.event
def connect(sid, environ, auth):
    print('---------------------------connect ', sid)

@sio.event
def disconnect(sid):
    print('---------------------------disconnect ', sid)

@sio.on('data')
def my_message(sid, data):
    print('message: ', data)
    sio.emit('Recebido-pelo-servidor')

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)