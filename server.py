import socketio
import eventlet
from ttgLib.TextToGcode import ttg

# Conversão do texto para Gcode:
fontScale = 0.5
offsetList = [
    (25, 49),
    (30, 40),
    (90, 40),
    (35, 32),
    (48, 32),
    (100, 32),
    (42, 24),
    (72, 24),
    (37, 16),
    (90, 16),
    (41, 7)
]

def offsetGcode(gcodeAbsolute, offsetX, offsetY):
    for i, command in enumerate(gcodeAbsolute):
        if 'X' in command or 'Y' in command:
            words = command.split(" ")
            for k in range(len(words)):
                if 'X' in words[k]:
                    finalX = int(words[k][1:])*fontScale+offsetX
                    words[k] = 'X' + str(finalX)
                if 'Y' in words[k]:
                    finalX = int(words[k][1:])*fontScale+offsetY
                    words[k] = 'Y' + str(finalX)

            gcodeAbsolute[i] = ""
            for j in range(len(words)):
                if j == len(words)-1:
                    gcodeAbsolute[i] += words[j]
                else:
                    gcodeAbsolute[i] += words[j] + " "

def createFormsGcode(form, cuttingSpeed, fontSize):
    finalGcode = []

    for i, entry in enumerate(form):
        if i == 0:
            path = ttg(entry, fontSize, 0, "return", cuttingSpeed).toGcode(
                "G1 Z0.5", "G1 Z5", "G0", "G1")
            offsetGcode(path, offsetList[i][0], offsetList[i][1])
            finalGcode = path[:3] + ["G1 Z5"] + path[3:]
        else:
            path = ttg(entry, fontSize, 0, "return", cuttingSpeed).toGcode(
                "G1 Z0.5", "G1 Z5", "G0", "G1")
            # Remove the first three lines
            path = path[3:]
            offsetGcode(path, offsetList[i][0], offsetList[i][1])
            finalGcode += path
    finalGcode[0] = 'G1 F200' 
    return finalGcode


# Server
sio = socketio.Server(cors_allowed_origins="*")
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
    sio.emit('recebido_forms', 'Recebido-pelo-servidor')
    # cria g-code
    # emite g-code criado
    finalGcode = createFormsGcode(data, 2000, 1)
    textoFinal = ""
    for command in finalGcode:
        textoFinal += command+"\n"
    sio.emit('gcode', textoFinal)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    eventlet.wsgi.server(eventlet.listen(('', port)), app)