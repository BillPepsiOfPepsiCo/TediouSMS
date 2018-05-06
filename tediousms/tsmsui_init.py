from tkinter import *
from tsmsui import Base_GUI, set_text, clear_text
from socket import gethostbyname, gethostname
from telesocket import *
from Telegraph import TelegraphKey
from RPi.GPIO import cleanup
import asyncio

#Credits to ya boi Chris Rice for the gorgeous user interface UI interface

DEFAULT_PORT = 42069 #nice meme

class CustomBase_GUI(Base_GUI):
	
	def __init__(self, root):
		Base_GUI.__init__(self, root)
		self._telesocket = None
		self._telegraph_key = None
		
	def on_send_button_clicked(self, *args):
		text = self.outbound_message_textbox.get("1.0", END)
		
		if len(text) > 0:
			self._telesocket.send_message(text)
		
	def recipient_ip_entry_field_invalidcommand(self, *args):
		print(args)
		
	def recipient_ip_entry_field_validatecommand(self, *args):
		print(args)
	
	def recipient_ip_entry_field_xscrollcommand(self, *args):
		pass
		
	def user_ip_entry_field_invalidcommand(self, *args):
		print(args)
		
	def user_ip_entry_field_validatecommand(self, *args):
		print(args)
		
	def user_ip_entry_field_xscrollcommand(self, *args):
		pass

	def outbound_message_textbox_xscrollcommand(self, *args):
		print(args)
		
	def outbound_message_textbox_yscrollcommand(self, *args):
		print(args)
		
	def inbound_message_textbox_xscrollcommand(self, *args):
		print(args)
		
	def inbound_message_textbox_yscrollcommand(self, *args):
		print(args)
		
	def listening_checkbox_command(self, *args):
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
					self._telegraph_key = TelegraphKey(16, 17, 27, 26, demo.outbound_message_textbox)
				else:
					print("Could not listen: user not connected to the Internet")
					self.listening_checkbox_value.set(0)
			else:
				print("Could not listen: invalid recipient IP address")
				self.recipient_ip_entry_field.configure(background = "red")
				self.listening_checkbox_value.set(0)
		else:
			if self._telesocket is not None and self._telesocket.server_running():
				print("Plugging ears")
				self._telesocket.stop_server_thread()
				self.send_button.configure(state = "disabled")
				self.recipient_ip_entry_field.configure(state = "normal")
				self._telegraph_key.__deinit()
			
	def listen_fail(self):
		self.listening_checkbox_value.set(0)
	
	def on_message_received(self, message):
		self.inbound_message_textbox.configure(state = "normal")
		self.inbound_message_textbox.delete('1.0', END)
		self.inbound_message_textbox.insert('1.0', message)
		self.inbound_message_textbox.configure(state = "readonly")
	
def main():
	root = Tk()
	demo = CustomBase_GUI(root)
	
	#Initialize the checkbox so we can read its value
	#This is super weird and overly complicated because
	#it has to come after the Tk() call unless you're on python 2
	demo.listening_checkbox_value = IntVar()
	demo.listening_checkbox.configure(variable = demo.listening_checkbox_value)
	
	root.title('TediouSMS')
	root.protocol('WM_DELETE_WINDOW', root.quit)

	
	if user_connected_to_network():
		set_text(demo.user_ip_entry_field, get_user_ip_address())
		
	else:
		set_text(demo.user_ip_entry_field, "Not connected to Internet")

	root.mainloop()

if __name__ == '__main__': main()
