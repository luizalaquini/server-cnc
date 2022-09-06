import socketio
import eventlet
from TextToGcode import ttg

# Conversão do texto para Gcode:
fontScale = 0.5
offsetList = [
    (30, 91), # MODELO
    (35, 83), # NUM SERIE
    (97, 83), # CAP DE CARGA
    (41, 75), # DATA DE FAB MES
    (54, 75), # DATA DE FAB ANO
    (106, 75), # CLASSE DE UTIL
    (48, 66), # ESTADO DE CARGA
    (77, 66), # PESO 
    (42, 58), # POT INSTALADA
    (97, 58), # VOLTAGEM
    (48, 49)  # N CREA
]
configs = [
    '$100=629.921', '$101=629.921', '$102=629.921', 
    '$110=420', '$111=420', '$112=420', 
    '$5=0', '$21=1', '$22=1', '$23=7', 
    '$120=40', '$121=40', '$122=40'
    ]
homing = ['$H', 'G92 X0 Y0 Z0']
zUP = 'G1 F450 Z29'
zDown = 'G1 F200 Z32.7'

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
                zDown, zUP, "G0", "G1")
            offsetGcode(path, offsetList[i][0], offsetList[i][1])
            finalGcode = path[:3] + [zUP] + path[3:]
        else:
            path = ttg(entry, fontSize, 0, "return", cuttingSpeed).toGcode(
                zDown, zUP, "G0", "G1")
            # Remove the first three lines
            path = path[3:]
            offsetGcode(path, offsetList[i][0], offsetList[i][1])
            finalGcode += path
    finalGcode[0] = 'G1 F400' 
    finalGcode = homing + configs + finalGcode + homing
    return finalGcode

# Server
sio = socketio.Server(cors_allowed_origins="*", )
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