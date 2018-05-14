from sys import exit

try:
	import websockets
except ImportError:
	print("Websockets 4.0 is not installed or is unavailable for this python installation. Please install with pip!")
	exit(0)

import socket, asyncio, struct, platform, pydoc
from socket import gethostbyname, gethostname
from threading import Thread

PREVIOUS_SERVER_ADDRESS = None

###################################################################
"""
Dear Dr. Cherry,

Hello. I'm sure you're looking at the final version of this file,
ignorant of the blood, sweat, tears, and StackOverflow queries that
went into creating this behemoth of behavior that required
an asynchronous task to run on its own thread that must be able
to be canceled at any time.
In python, async wasn't even a full-fledged thing until python 3,
so I had to learn everything about python's hilariously inadequate and
confusing version of async. Then, I had to learn how to get an async
event loop to run on its own thread. Then, I had to learn how to
ensure the thread could exit on its own whenever I wanted. That...
...was really, really hard. Probably took me longer than learning
how to use websockets. Now, why did I write this long-winded paragraph
in a random supporting file of my magnificently unintuitive SMS client?
Why did I decide to address you directly at the top of a random module
that plays a core role in allowing this program to communicate
over a network connection?

I'd just like some cool guy points.

Thanks,
Brennan
"""
###################################################################
class Telesocket(object):

	def __init__(self, host_ip, host_port, recipient_ip, recipient_port, message_consumer):
		"""
		Creates a new instance of the super intuitive Telesocket.
		
		Keyword arguments:
		host_ip (str) => a valid IPV4 address that the server will be listening on (the IP the machine this is running on is). See Telesocket.get_user_ip_address()
		host_port (int) => the port the server will listen on.
		recipient_ip (str) => a valid IPV4 address that send_message calls will attempt to connect and send a message to.
		recipient_port (int) => the port the recipient is listening on.
		message_consumer (function) => a function that's called each time the server recieves a message. Called with 1 parameter, a str (the message).
		"""
		
		self._host_ip = host_ip
		self._host_port = host_port
		self._recipient_ip = recipient_ip
		self._recipient_port = recipient_port
		self._message_consumer = message_consumer
		self._server_thread = None
		self._loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self._loop)

		print("Telesocket initialized (host: %s client: %s)" % (self.host_uri(), self.client_uri()))
	
	async def listen(self, websocket, path):
		"""
		The asynchronous function that handles the actual websocket listening and thread monitoring.
		Also handles closing the thread.
		
		Keyword arguments:
		websocket => the websocket to listen on.
		path => I'm not really sure, but the callback from serving on the websocket gives 2 paremeters so it has to be there.
		"""
		async for message in websocket:
			try:
				self._message_consumer(message)
			except TypeError:
				raise TypeError("The message consumer (%s) for your Telesocket takes too many or too few arguments. (Should be 1)" % str(self._message_consumer))
		
	def start_server_thread(self):
		"""
		Creates a new daemon thread that listens on the specified host_ip and host_port.
		Can be gracefully and safely shutdown at any time with Telesocket.stop_server_thread()
		"""
		
		global PREVIOUS_SERVER_ADDRESS #A poorly advised global variable that allows host address "reuse"
		
		if self._server_thread == None:
			print("Creating server thread")
			
			#This is where the websocket binds to the host_ip. Since websockets abstracts the usual
			#low-level socket API, I can't directly tell the socket API to allow address reuse,
			#so, instead, the Telesocket will simply not try to bind to the IP address if the specified host_ip
			#is the last address the websocket bound to.
			if PREVIOUS_SERVER_ADDRESS is None or not (PREVIOUS_SERVER_ADDRESS == self.host_ip):
				self._loop.run_until_complete(websockets.serve(self.listen, self.host_ip, self.host_port))
				PREVIOUS_SERVER_ADDRESS = self.host_ip
				
			self._server_thread = Thread(target = self._loop.run_forever, daemon = True)
		
		if self.server_running():
			print("Server thread start attempted but it\'s running already, ignoring")
		else:
			print("Starting server thread")
			self._server_thread.start()
	
	def stop_server_thread(self):		
		"""
		If the server thread has been started, gracefully stops it. This can be done at any time with no risk since it's
		just a listener that calls a synchronous function. 
		"""
		
		if self.server_running():
			print("Stopping server thread")
			self._loop.call_soon_threadsafe(self._loop.stop)
			self._server_thread.join()
			#It looks strange, but this is actually the easiest way to do it,
			#since the start_server_thread function makes a new Thread instance
			#if the server thread is None, and threads that are finished/canceled
			#cannot be started again.
			self._server_thread = None
		else:
			print("Server thread exit attempted but it\'s not running, ignoring")
			
	async def connect_and_send(self, message):
		"""
		The asynchronous function responsible for connecting to the specified recipient ip and port
		and sending a message.
		"""
		
		try:
			async with websockets.connect(self.client_uri(), timeout = 10) as websocket:
				print("Connection to %s successfully established" % self.client_uri())
				await websocket.send(message)
				print("Sent message => %s\nTo recipient => %s" % (message, self.client_uri()))
				
		except TimeoutError:
			print("It appears there is no open server at", self.client_uri())
		except ConnectionRefusedError:
			print("Connection to %s refused." % self.client_uri())
			
	
	def send_message(self, message):
		"""
		The function you want to call when you want to send a message to the (hopefully listening)
		recipient_ip and recipient_port.
		"""
		
		asyncio.new_event_loop().run_until_complete(self.connect_and_send(message))
	
	def host_uri(self):
		"""
		Returns a websocket 4.0 friendly URI with the host IP and port.
		"""
		
		return self.uri(self.host_ip, self.host_port)
	
	def client_uri(self):
		"""
		Returns a websocket 4.0 friendly URI with the recipient IP and port.
		"""
		
		return self.uri(self.recipient_ip, self.recipient_port)
	
	def uri(self, ip, port):
		"""
		The URI function used in creating URIs. 
		"""
		
		return "ws://%s:%s" % (ip, port)
	
	def server_running(self):
		"""
		Returns true if the server thread is alive,
		false if it hasn't been initialized or if it's dead.
		"""
		
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

def is_valid_ip(ip_address):
	"""
	Returns True if the ip_address is a valid IPV4 addresss, otherwise returns False.
	"""
	
	try:
		socket.inet_aton(ip_address)
		return True
	except socket.error:
		return False

def user_connected_to_network(host = "8.8.8.8", port = 53, timeout = 10):
	"""
	Returns True if the user successfully reaches the host and recieves a response.
	
	Keyword arguments:
	host => The IP of the host to reach (default is 8.8.8.8).
	port => The port of the host (default is 53).
	timeout => The timeout of the connection (default 10).
	"""

	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print("User does not appear to be connected to a network (DNS at 8.8.8.8:53 timed out after 3s)")
		print(ex.args)
		return False

def get_user_ip_address():
	"""
	Returns the IP of the user if they are connected to a network, otherwise returns None.
	"""
	
	if not user_connected_to_network():
		return None

	cur_platform = platform.platform()
	
	if "Linux" in cur_platform:
		return get_ip_linux()
	elif "Windows" in cur_platform:
		return get_ip_windows()

def get_ip_linux(host = "8.8.8.8", port = 53):
	"""
	Returns the IP of a user if they are on a Linux machine.
	
	Keyword arguments:
	host => The host required to connect to in order to get the user's IP without having to know what interface they're using (default is 8.8.8.8).
	port => The port to try and reach (default is 53).
	"""
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((host, port))
	return s.getsockname()[0]
		
def get_ip_windows():
	"""
	Gets the IP of the user on a Windows machine.
	On Linux, this always returns localhost.
	"""
	return gethostbyname(gethostname())
