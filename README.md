# Server CNC
![GitHub](https://img.shields.io/github/license/luizalaquini/server-cnc)
![GitHub repo size](https://img.shields.io/github/repo-size/luizalaquini/server-cnc)
![GitHub language count](https://img.shields.io/github/languages/count/luizalaquini/server-cnc)
![GitHub top language](https://img.shields.io/github/languages/top/luizalaquini/server-cnc)
![GitHub followers](https://img.shields.io/github/followers/luizalaquini?label=follow&style=social)

Running Page:

https://server-cnc.herokuapp.com/ (Not Working)

https://server-75ps4q3vc-luizalaquini.vercel.app/

### Usage
This server receives information (text) from a form, converts it to g-code and send it to esp8266 for usage at a CNC machine.

### Technologies
- Python
- Socket.io

### Behavior
When the server receives the 'data' event from the form, it transforms the array of strings received into G-Code, which are the final instructions to the CNC, and performs an emit through socketio of all commands to the esp8266.

The conversion of strings into G-code is done with an adaptation of the library TextToGcode available on github. This library checks character by character in a string and defines “manually” what commands are needed to draw that character. After that, an offset on the X axis is added depending on the character's position in the string and the scale is changed depending on a scale passed as a parameter - defining the font size.

With the converted strings, we create a code ( function offsetGcode() ) that receives the gcode to draw a word and adds an offset in the x-axis and y-axis, the which allows us to modify where that string will be written to on the board. For determine the values of these offsets, we use the cnc itself, moving its tip on the plate fields and noting the values of the positions in relation to the origin.

### Developers
- Luiza Batista Laquini (LinkedIn: https://www.linkedin.com/in/luizalaquini/)
- Guilherme Goes Zanetti (LinkedIn: https://www.linkedin.com/in/guilherme-goes-zanetti-0429631a2/)
- Joana Venturin Loureiro (LinkedIn: https://www.linkedin.com/in/joana-venturin-loureiro/)
