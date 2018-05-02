from tkinter import *
from tsmsui import Base_GUI, set_text, clear_text
from socket import gethostbyname, gethostname
from telesocket import Telesocket

#Credits to ya boi Chris Rice for the gorgeous user interface UI interface
class CustomBase_GUI(Base_GUI):
    
	def on_send_button_clicked(self, *args):
		print(args)
		
	def recipient_ip_entry_field_invalidcommand(self, *args):
		print(args)
		
	def recipient_ip_entry_field_validatecommand(self, *args):
		print(args)
	

	valid_chars = [range(0, 10)] + ["."]
	def recipient_ip_entry_field_xscrollcommand(self, *args):
		index = self.recipient_ip_entry_field.index(INSERT)

		if index > 0:
			new_char = self.recipient_ip_entry_field.get()[index - 1]
			print(new_char + " => " + str(type(new_char)))
			if str(new_char) in self.valid_chars:
				print("VALID CHAR")
		
	def user_ip_entry_field_invalidcommand(self, *args):
		print(args)
		
	def user_ip_entry_field_validatecommand(self, *args):
		print(args)
		
	def user_ip_entry_field_xscrollcommand(self, *args):
		print(args)

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
			#If checkbox is unchecked
		else:
			#If the checkbox is checked
	
def main():
	root = Tk()
	demo = CustomBase_GUI(root)
	
	#Initialize the checkbox so we can read its value
	#This is super weird and overly complicated because
	#it has to come after the Tk() call unless you're on python 2
	demo.listening_checkbox_value = IntVar()
	demo.listening_checkbox.configure(variable = demo.listening_checkbox_value)
	
	root.title('TediouSMS')
	try: run()
	except NameError: pass
	root.protocol('WM_DELETE_WINDOW', root.quit)
	set_text(demo.user_ip_entry_field, gethostbyname(gethostname()))
	root.mainloop()

if __name__ == '__main__': main()
