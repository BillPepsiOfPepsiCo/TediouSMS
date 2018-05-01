import asyncio
import socket
from socket import gethostbyname, gethostname


class Telesocket(object):

	def __init__(self, host_ip, host_port, recipient_ip, recipient_port):
		self._host_ip = host_ip
		self._host_port = host_port
		self._recipient_ip = recipient_ip
		self._recipient_port = recipient_port
		
	async def initialize_server(self):
		print("Initializing TediouSMS listener on %s" % self.host_ws_url())
		
		try:
			start_server = websockets.serve(recieve_message, self.host_ip, self.host_port)
			asyncio.get_event_loop().run_until_complete(start_server)
			asyncio.get_event_loop().run_forever()
		except Exception as ex:
			print("An error occurred while trying to initialize a TediouSMS listener on %s: " % self.host_ws_url())
			print(ex.args)
		
	async def close_server(self):
		print("Closing TediouSMS listener on %s" % self.host_ws_url())
		asyncio.get_event_loop().close()
		
	async def send_message(self, message):
		async with websockets.connect(self.client_ws_url()) as websocket:
			message = "_______"
			await websocket.send(message)
	
	async def recieve_message(self, websocket, path):
		message = await websocket.recv()
		return message
	
	def host_ws_url(self):
		return "ws://%s:%s" % (self.host_ip, self.host_port)
		
	def client_ws_url(self):
		return "ws://%s:%s" % (self.recipient_ip, self.recipient_port)
	
	@property
	def host_ip(self):
		return self._host_ip
	
	@property
	def host_port(self):
		return self._host_port
	
	@property
	def recipient_ip(self):
		return self._recipient_ip
		
	@property
	def recipient_port(self):
		return self._recipient_port

#Returns true if Google's DNS is successfully reached and False otherwise.
#A good indicator of whether or not the user is connected to a network.
def user_connected_to_network(host = "8.8.8.8", port = 53, timeout = 3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print("User does not appear to be connected to a network (DNS at 8.8.8.8:53 timed out after 3s)")
		print(ex.message)
		return False

#Returns if the specified string is a valid IP address (including 'localhost')
def verify_ip_address(ip_address):
	substring = ip_address.split(":")[0]
	
	
#Returns the user's current IP address
#returns None if the user is not connected to a network
def get_user_ip_address():
	if user_connected_to_network():
		return gethostbyname(gethostname())
	else:
		return None