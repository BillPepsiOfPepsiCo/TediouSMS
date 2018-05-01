from ..telesocket import *
from time import sleep as shleep

big_socc = Telesocket("localhost", 42069, "localhost", 42069, print)

big_socc.start_server_thread()
shleep(30)
big_socc.stop_server_thread()