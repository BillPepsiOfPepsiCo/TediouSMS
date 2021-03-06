from sys import exit, version_info
import asyncio, pydoc

try:
	import RPi.GPIO as GPIO
except ImportError:
	print("Either you don\'t have the GPIO headers installed or you\'re not running this program on a Raspberry Pi. Please fix!")
	exit(0)
	
from tkinter import *
from tsmsui import Base_GUI, set_text, clear_text
from socket import gethostbyname, gethostname
from telesocket import *
from Telegraph import *
from websockets import *
from time import sleep
#Credits to ya boi Chris Rice for the gorgeous user interface UI interface

DEFAULT_PORT = 1337 #nice meme

button_list = list(range(1, 10)) + ["0", ".", "<="]

class NumberPad(Frame):
	
	def __init__(self, root, widget_to_type_in_to):
		"""Initializes a new NumberPad.
		
		Arguments:
		root => the root window this will be spawned inside of.
		widget_to_type_in_to => the widget the buttons of this numpad will write to.
		"""
		
		Frame.__init__(self, root)
		self.root = root
		self.root.title("IP")
		self.grid()
		self.create_layout()
		self.widget_to_type_in_to = widget_to_type_in_to
			
	def create_layout(self):
		"""Creates the layout of the numberpad."""
		
		r = 1
		c = 0
		
		for number in button_list:
			if number == "<=":
				command = lambda: self.widget_to_type_in_to.delete(len(self.widget_to_type_in_to.get()) - 1, END)
			else:
				command = lambda char = number: self.widget_to_type_in_to.insert(INSERT, char)
				
			self.button = Button(self, text = number, width = 5, height = 4, command = command).grid(row = r, column = c)
			c += 1

			if c > 2:
				c = 0
				r += 1
	
class CustomBase_GUI(Base_GUI):
	
	def __init__(self, root):
		"""
		Initialize this GUI class.
		Tosses up the call to the Base_GUI.
		"""
		
		Base_GUI.__init__(self, root)
		self.root = root
		self._telesocket = None
		self._telegraph_key = None
		self._numpad = None
	
	def on_send_button_clicked(self, *args):
		"""
		The callback for the send button.
		Simply instructs the telesocket to send the message to its recipient_ip.
		"""
		
		text = self.outbound_message_textbox.get("1.0", END)
		
		if len(text) > 0:
			self._telesocket.send_message(text)
		
	def listening_checkbox_command(self, *args):
		"""
		The callback for the checkbox that says "listening on IP"
		Checks if the user is connected to the internet and initializes a telesocket
		with the specified recipient ip if they are.
		"""
		
		if self.listening_checkbox_value.get():
			print("Time for some serious protection.")
			print("Validating client IP address")
			client_ip = self.recipient_ip_entry_field.get()
			
			if is_valid_ip(client_ip):
				self.recipient_ip_entry_field.configure(background = "white")
				
				if user_connected_to_network():
					print("Initializing Telesocket(TM)")
					self._telesocket = Telesocket(get_user_ip_address(), DEFAULT_PORT, client_ip, DEFAULT_PORT, self.on_message_received)					
					self._telesocket.start_server_thread()
					self.send_button.configure(state = "normal")
					self.recipient_ip_entry_field.configure(state = "readonly")
					self._telegraph_key = TelegraphKey(16, 17, 27, 26, self.outbound_message_textbox)
				else:
					print("Could not listen: user not connected to the Internet")
					self.listen_fail()
			else:
				print("Could not listen: invalid recipient IP address")
				self.recipient_ip_entry_field.configure(background = "red")
				self.listen_fail()
		else:
			if self._telesocket is not None and self._telesocket.server_running():
				print("Plugging ears")
				self._telesocket.stop_server_thread()
				self.send_button.configure(state = "disabled")
				self.recipient_ip_entry_field.configure(state = "normal")
				self._telegraph_key._deinit()
	
	def listen_fail(self):
		"""
		Called when listening is unable to start for whatever reason.
		Simply resets the checkbox to its off state.
		"""
		
		self.listening_checkbox_value.set(0)
	
	def on_message_received(self, message):
		"""
		The callback supplied to the Telesocket.
		Called whenever the Telesocket recieves a message.
		This is where the beeps and boops are made.
		"""
		
		self.inbound_message_textbox.configure(state = "normal")
		self.inbound_message_textbox.delete('1.0', END)
		self.inbound_message_textbox.insert('1.0', message)
		
		for char in message:
			sleep(0.1)
			
			if char == DOT:
				self._telegraph_key._750_Hz_tone.play(-1)
				GPIO.output(self._telegraph_key.incoming_message_indicator_pin, GPIO.HIGH)			
				sleep(UNIT_LENGTH)
			elif char == DASH:
				self._telegraph_key._750_Hz_tone.play(-1)
				GPIO.output(self._telegraph_key.incoming_message_indicator_pin, GPIO.HIGH)			
				sleep(DASH_LENGTH)
			elif char == " ":
				sleep(LETTER_SPACE_LENGTH)
			elif char == "/":
				sleep(WORD_SPACE_LENGTH)

			self._telegraph_key._750_Hz_tone.stop()
			GPIO.output(self._telegraph_key.incoming_message_indicator_pin, GPIO.LOW)
				
		self.inbound_message_textbox.configure(state = "disabled")
		
	def on_focus_gained(self, event):
		"""This is where the NumberPad is spawned.
		Called whenever any widget gets focused, but
		only selecting the ip entry field actually does something.
		"""
		
		if self._numpad is None and event.widget == self.recipient_ip_entry_field:
			print("I have achieved focus")
			self._numpad = NumberPad(Tk(), self.recipient_ip_entry_field)
			#This prevents more than 1 numpad from being spawned at a time by not responding to additional focus events
			#until the focus event is rebound in the on_numpad_closed function.
			#The expression lambda: None is basically how you pass an empty function with lambdas.
			#Functions that don't return anything return None, and lambda functions have to return
			#something to be a complete expression.
			self.root.bind("<FocusIn>", lambda event: None)
			self._numpad.root.bind("<Destroy>", self.on_numpad_closed)
			
	def on_numpad_closed(self, event):
		"""A function that re-binds the focus event since it has
		to be unbound to prevent a looping window.
		"""
		self.send_button.focus_set()
		self._numpad = None
		#Rebind the focus event to the correct function whenever the numpad is closed.
		self.root.bind("<FocusIn>", self.on_focus_gained)

if __name__ == '__main__': 
	if version_info >= (3, 6):
		GPIO.setmode(GPIO.BCM)
		root = Tk()
		demo = CustomBase_GUI(root)
		
		#Initialize the checkbox so we can read its value
		#This is super weird and overly complicated because
		#it has to come after the Tk() call unless you're on python 2
		demo.listening_checkbox_value = IntVar()
		demo.listening_checkbox.configure(variable = demo.listening_checkbox_value)
		
		root.title('TediouSMS')
		root.protocol('WM_DELETE_WINDOW', root.quit)
		root.bind("<FocusIn>", demo.on_focus_gained)

		if user_connected_to_network():
			set_text(demo.user_ip_entry_field, get_user_ip_address())
		else:
			set_text(demo.user_ip_entry_field, "Not connected to Internet")

		root.mainloop()
	else:
		print("Python 3.6 and above is required to run TediouSMS.")
		exit(0)
