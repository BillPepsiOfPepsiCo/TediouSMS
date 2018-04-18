import RPi.GPIO as GPIO

class TelegraphKey(object):

	def __init__(self, pin):
		self.pin = pin

	#Begins listening on whatever port this is initialized on for button presses.
	def listen(self):
		while True:
			while GPIO.input(self.pin):
				