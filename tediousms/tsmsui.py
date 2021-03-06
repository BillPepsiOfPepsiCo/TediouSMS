import os
from tkinter import *

#Credits to ya boi Chris Rice for the gorgeous user interface UI interface
class Base_GUI(object):

	_images = []
	
	def __init__(self, root):

		# Widget Initialization
		self.sending_label = Label(root,
			font = "{MS Sans Serif} 14 bold",
			text = "Sending",
		)
		
		self.receiving_label = Label(root,
			font = "{MS Sans Serif} 14 bold",
			text = "Receiving",
		)

		self.send_button = Button(root,
			font = "{MS Sans Serif} 14 bold",
			text = "SEND",
			state = "disabled",
		)
		
		self.recipient_ip_entry_field = Entry(root,
			width = 0,
		)
		
		self.recipient_ip_address_label = Label(root,
			font = "{MS Sans Serif} 12",
			text = "Recipient IP Address",
		)
		
		self.user_ip_address_label = Label(root,
			font = "{MS Sans Serif} 12",
			text = "Your IP Address",
		)
		
		self.outbound_message_textbox = Text(root,
			height = 0,
			width = 0,
			state = "disabled",
		)
				
		self.inbound_message_textbox = Text(root,
			height = 0,
			width = 0,
			state = "disabled",
		)
		
		self.user_ip_entry_field = Entry(root,
			width = 0,
			state = "readonly",
		)
		
		self.listening_checkbox = Checkbutton(root,
			font = "{MS Sans Serif} 12 bold",
			text = "Listening on IP",
		)

		# widget commands

		self.send_button.configure(
			command = self.on_send_button_clicked
		)
		
		self.listening_checkbox.configure(
			command = self.listening_checkbox_command
		)
		
		# Geometry Management
		self.sending_label.grid(
			in_	   = root,
			column = 1,
			row	   = 1,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)
		
		self.receiving_label.grid(
			in_	   = root,
			column = 2,
			row	   = 1,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)
		
		self.send_button.grid(
			in_	   = root,
			column = 1,
			row	   = 3,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)
		
		self.recipient_ip_entry_field.grid(
			in_	   = root,
			column = 2,
			row	   = 5,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = "ew"
		)
		
		self.recipient_ip_address_label.grid(
			in_	   = root,
			column = 2,
			row	   = 4,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)
		
		self.user_ip_address_label.grid(
			in_	   = root,
			column = 1,
			row	   = 4,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)
		
		self.outbound_message_textbox.grid(
			in_	   = root,
			column = 1,
			row	   = 2,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = "news"
		)
		
		self.inbound_message_textbox.grid(
			in_	   = root,
			column = 2,
			row	   = 2,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = "news"
		)
		
		self.user_ip_entry_field.grid(
			in_	   = root,
			column = 1,
			row	   = 5,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = "ew",
		)
		
		self.listening_checkbox.grid(
			in_	   = root,
			column = 2,
			row	   = 3,
			columnspan = 1,
			ipadx = 0,
			ipady = 0,
			padx = 0,
			pady = 0,
			rowspan = 1,
			sticky = ""
		)


		# Resize Behavior
		root.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
		root.grid_rowconfigure(2, weight = 0, minsize = 133, pad = 0)
		root.grid_rowconfigure(3, weight = 0, minsize = 102, pad = 0)
		root.grid_rowconfigure(4, weight = 0, minsize = 21, pad = 0)
		root.grid_rowconfigure(5, weight = 0, minsize = 30, pad = 0)
		root.grid_rowconfigure(6, weight = 0, minsize = 2, pad = 0)
		root.grid_columnconfigure(1, weight = 0, minsize = 200, pad = 0)
		root.grid_columnconfigure(2, weight = 0, minsize = 200, pad = 0)

"""
Text mutators.
Automatically enables and disables text widgets to ensure they
maintain state after editing is complete.
"""

#Clears the text of the specified tkinter text widget.
def clear_text(widget):
	do_thing_with_text_preserve_state(widget, widget.delete, 0, END)

#"Sets," i.e. clears the current text and then appends, the specified text
#to the specified tkinter text widget.
def set_text(widget, text):
	clear_text(widget)
	do_thing_with_text_preserve_state(widget, widget.insert, 0, text)

#Adds text to a tkinter text widget without removing any text beforehand.
def append_text(widget, text):
	do_thing_with_text_preserve_state(widget, widget.insert, INSERT, text)
	
def do_thing_with_text_preserve_state(widget, thing, index, text):
	old_state = get_state(widget)
	
	widget.config(state = "normal")
	thing(index, text)
	widget.config(state = old_state)

#Returns true if disabled, false if enabled.
def get_state(widget):
	return widget["state"]


