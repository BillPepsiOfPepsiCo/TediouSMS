# TediouSMS
Probably the least intuitive simultaneous messaging service ever created.

# Planned features:

Simultaneous messaging over IP with morse code messages

# Dependencies:

Python 3.6

websockets 4.0

Tk/Tcl 8

# Notes:

Installation on a Raspberry Pi requires the installation of Python 3.6, but Raspbian
comes with Python 3.5 installed. **TediouSMS will NOT work on a Python 3.5 installation.**

I've automated this. Please just run ```sh install_dependencies.sh```. It will take a long time.

# Limitations:

While, technically (and practically, you can try this yourself) a listening client can
recieve messages from any number of other clients trying to send messages to it, a client
can only send messages to 1 other client at a time. Maybe I'll fix this in the future
but there is actually no point given the scope of this project.