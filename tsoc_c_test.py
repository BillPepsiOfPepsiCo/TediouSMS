from ..telesocket import *

big_socc = Telesocket("localhost", 42069, "localhost", 42069, print)

big_socc.send_message("Hey! A message!")