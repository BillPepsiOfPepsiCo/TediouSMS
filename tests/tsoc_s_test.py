import sys
sys.path.append('../')
from time import sleep as shleep
from tediousms import telesocket

if __name__ == "__main__":
	big_socc = telesocket.Telesocket("localhost", 42069, "localhost", 42069, print)

	big_socc.start_server_thread()
	shleep(30)
	big_socc.stop_server_thread()