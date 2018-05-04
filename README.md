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
comes with Python 3.5 installed. **TediouSMS will NOT work on a Python 3.6 installation.**

Unfortunately, Python 3.6 has no release target for Raspbian, so you have to download
and compile it yourself (or run the `install_dependencies` script). Building Python from
source and using the `tkinter` libraries requires the installation of `tk-dev` before
compiliation:

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install tk-dev```

I'm not actually sure if that works, so in the near future (next day or 2) I'm going to
figure out how to acquire it from somewhere that's not apt. 

I'll probably download the Tcl release [here](https://www.tcl.tk/software/tcltk/download.html).
and learn how to compile it [here](https://www.tcl.tk/doc/howto/compile.html).

This will, of course, eventually be automated by the `install_dependencies` script.

# Limitations:

While, technically (and practically, you can try this yourself) a listening client can
recieve messages from any number of other clients trying to send messages to it, a client
can only send messages to 1 other client at a time. Maybe I'll fix this in the future
but there is actually no point given the scope of this project.