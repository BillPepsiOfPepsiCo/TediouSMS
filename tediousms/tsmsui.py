import tkinter as Tkinter
from tkinter import *
import os

#Credits to ya boi Chris Rice for the gorgeous user interface UI interface
class Base_GUI(object):

	_images = []
	
	def __init__(self, root):

		# Widget Initialization
		self.sending_label = Tkinter.Label(root,
			font = "{MS Sans Serif} 14 bold",
			text = "Sending",
		)
		
		self.receiving_label = Tkinter.Label(root,
			font = "{MS Sans Serif} 14 bold",
			text = "Receiving",
		)

		self.send_button = Tkinter.Button(root,
			font = "{MS Sans Serif} 14 bold",
			text = "SEND",
			state = "disabled",
		)
		
		self.recipient_ip_entry_field = Tkinter.Entry(root,
			width = 0,
		)
		
		self.recipient_ip_address_label = Tkinter.Label(root,
			font = "{MS Sans Serif} 12",
			text = "Recipient IP Address",
		)
		
		self.user_ip_address_label = Tkinter.Label(root,
			font = "{MS Sans Serif} 12",
			text = "Your IP Address",
		)
		
		self.outbound_message_textbox = Tkinter.Text(root,
			height = 0,
			width = 0,
			state = DISABLED,
		)
				
		self.inbound_message_textbox = Tkinter.Text(root,
			height = 0,
			width = 0,
			state = NORMAL,
		)
		
		self.user_ip_entry_field = Tkinter.Entry(root,
			width = 0,
			state = NORMAL,
		)
		
		self.listening_checkbox = Tkinter.Checkbutton(root,
			font = "{MS Sans Serif} 12 bold",
			text = "Listening on IP",
		)

		# widget commands

		self.send_button.configure(
			command = self.on_send_button_clicked
		)
		
		self.recipient_ip_entry_field.configure(
			invalidcommand = self.recipient_ip_entry_field_invalidcommand
		)
		
		self.recipient_ip_entry_field.configure(
			validatecommand = self.recipient_ip_entry_field_validatecommand
		)
		
		self.recipient_ip_entry_field.configure(
			xscrollcommand = self.recipient_ip_entry_field_xscrollcommand
		)
		
		self.user_ip_entry_field.configure(
			invalidcommand = self.user_ip_entry_field_invalidcommand
		)
		
		self.user_ip_entry_field.configure(
			validatecommand = self.user_ip_entry_field_validatecommand
		)
		
		self.user_ip_entry_field.configure(
			xscrollcommand = self.user_ip_entry_field_xscrollcommand
		)
		
		self.outbound_message_textbox.configure(
			xscrollcommand = self.outbound_message_textbox_xscrollcommand
		)
		
		self.outbound_message_textbox.configure(
			yscrollcommand = self.outbound_message_textbox_yscrollcommand
		)
		
		self.inbound_message_textbox.configure(
			xscrollcommand = self.inbound_message_textbox_xscrollcommand
		)
		
		self.inbound_message_textbox.configure(
			yscrollcommand = self.inbound_message_textbox_yscrollcommand
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
	read_only = check_state(widget)

	if read_only:
		widget.config(state = "normal")

	widget.delete(0, END)

	if read_only:
		widget.config(state = "readonly")

#"Sets," i.e. clears the current text and then appends, the specified text
#to the specified tkinter text widget.
def set_text(widget, text):
	read_only = check_state(widget)

	if read_only:
		widget.config(state = "normal")

	clear_text(widget)
	widget.insert(0, text)

	if read_only:
		widget.config(state = "readonly")

#Adds text to a tkinter text widget without removing any text beforehand.
def append_text(widget, text, read_only):
	read_only = check_state(widget)

	if read_only:
		widget.config(state = "normal")

	widget.insert(INSERT, text)

	if read_only:
		widget.config(state = "readonly")

#Returns true if disabled, false if enabled.
def check_state(widget):
	return	widget["state"] == "disabled"


