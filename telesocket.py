import socket
from socket import gethostbyname, gethostname

def user_connected_to_network(host = "8.8.8.8", port = 53, timeout = 3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print("User does not appear to be connected to a network (DNS at 8.8.8.8:53 timed out after 3s)")
		print(ex.message)
		return False

def get_user_ip_address():
	return gethostbyname(gethostname())