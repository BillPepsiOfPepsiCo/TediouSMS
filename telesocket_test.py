import telesocket
from telesocket import *

big_socc = Telesocket("localhost", 42069, "localhost", 69420)

big_socc.initialize_server()
print("Server made boi")