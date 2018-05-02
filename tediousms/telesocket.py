import socket
from socket import gethostbyname, gethostname
from threading import Thread
import asyncio
import websockets

class Telesocket(object):

	"""
	Creates a new instance of the super intuitive Telesocket.
	host_ip (str) => a valid IPV6 address that the server will be listening on (the IP the machine this is running on is). See Telesocket.get_user_ip_address()
	host_port (int) => the port the server will listen on.
	recipient_ip (str) => a valid IPV6 address that send_message calls will attempt to connect and send a message to.
	recipient_port (int) => the port the recipient is listening on.
	message_consumer (function) => a function that's called each time the server recieves a message. Called with 1 parameter, a str (the message).
	"""
	def __init__(self, host_ip, host_port, recipient_ip, recipient_port, message_consumer):
		self._host_ip = host_ip
		self._host_port = host_port
		self._recipient_ip = recipient_ip
		self._recipient_port = recipient_port
		self._message_consumer = message_consumer
		self._server_thread = None
		self._loop = asyncio.new_event_loop()

		print("Telesocket initialized (host: %s client: %s)" % (self.host_uri(), self.client_uri()))
	
	"""
	Launches a server that listens on the specified host_ip and host_port.
	This is not the threaded version. If you intend to run a Telesocket server
	on its own thread, see Telesocket.start_server_thread()
	"""
	def begin_listening(self):
		print("Internet connection found, launching server")
			asyncio.set_event_loop(self._loop)
			self._loop.run_until_complete(websockets.serve(self.listen, self.host_ip, self.host_port))
			print("Telesocket server listening on", self.host_uri())
			self._loop.run_forever()
	
	"""
	The asynchronous function that handles the actual websocket listening and thread monitoring.
	Also handles closing the thread.
	"""
	async def listen(self, websocket, path):
		if getattr(self._server_thread, "do_run", True):
			async for message in websocket:
				try:
					self._message_consumer(message)
				except TypeError:
					raise TypeError("The message consumer (%s) for your Telesocket takes too many or too few arguments. (Should be 1)" % str(self._message_consumer))
		else:
			return
		
	"""
	Creates a new daemon thread that listens on the specified host_ip and host_port.
	Can be gracefully and safely shutdown at any time with Telesocket.stop_server_thread()
	"""
	def start_server_thread(self):
		if self._server_thread == None:
			print("Creating server thread")
			self._server_thread = Thread(target = self.begin_listening, daemon = True)
			self._server_thread.do_run = True
		
		if self._server_thread.isAlive():
			print("Server thread start attempted but it\'s running already, ignoring")
		else:
			print("Starting server thread")
			self._server_thread.start()
	
	"""
	If the server thread has been started, gracefully stops it. This can be done at any time with no risk since it's
	just a listener that calls a synchronous function. 
	"""
	def stop_server_thread(self):		
		if self._server_thread.isAlive():
			print("Stopping server thread")
			self._server_thread.do_run = False
		else:
			print("Server thread exit attempted but it\'s not running, ignoring")
	
	"""
	The asynchronous function responsible for connecting to the specified recipient ip and port
	and sending a message.
	"""
	async def connect_and_send(self, message):
		try:
			async with websockets.connect(self.client_uri()) as websocket:
				print("Connection to %s successfully established" % self.client_uri())
				await websocket.send(message)
				
		except Exception as e:
			print("An exception occurred while trying to establish a connection and send a message: ")
			print(e.args)
	
	"""
	The function you want to call when you want to send a message to the (hopefully listening)
	recipient_ip and recipient_port.
	"""
	def send_message(self, message):
		asyncio.get_event_loop().run_until_complete(self.connect_and_send(message))
	
	"""
	Returns a websocket 4.0 friendly URI with the host IP and port.
	"""
	def host_uri(self):
		return self.uri(self.host_ip, self.host_port)
		
	"""
	Returns a websocket 4.0 friendly URI with the recipient IP and port.
	"""
	def client_uri(self):
		return self.uri(self.recipient_ip, self.recipient_port)
	
	"""
	The URI function used in creating URIs. 
	"""
	def uri(self, ip, port):
		return "ws://%s:%s" % (ip, port)
	
	"""
	Returns true if the server thread is alive,
	false if it hasn't been initialized or if it's dead.
	"""
	def server_running(self):
		if self._server_thread == None:
			return False
		else:
			return self._server_thread.is_alive()
	
	"""
	Accessors / mutators
	"""
	
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
		print(ex.args)
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