from socket import gethostbyname, gethostname
import asyncio
import websockets

class Telesocket(object):

	def __init__(self, host_ip, host_port, recipient_ip, recipient_port):
		self._host_ip = host_ip
		self._host_port = host_port
		self._recipient_ip = recipient_ip
		self._recipient_port = recipient_port
		
	async def listen(self, websocket, path):
		async for message in websocket:
			consume_message(message)
				
	def consume_message(self, message):
		print("Consuming message => " + message)
	
	def serve(self):
		print("")
		asyncio.get_event_loop().run_until_complete(websockets.serve(self.listen, self.host_ip, self.host_port))
		asyncio.get_event_loop().run_forever()
		
	async def connect_and_send(self, message):
		try:
			async with websockets.connect(self.client_uri()) as websocket:
				await websocket.send(message)
		except Exception as e:
			print("An exception occurred while trying to establish a connection and send a message: ")
			print(e.args)
	
	def send_message(self, message):
		asyncio.get_event_loop().run_until_complete(self.connect_and_send(message))
	
	def host_uri(self):
		return self.uri(self.host_ip, self.host_port)
		
	def client_uri(self):
		return self.uri(self.recipient_ip, self.recipient_port)
		
	def uri(self, ip, port):
		return "ws://%s:%s" % (ip, port)
	
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