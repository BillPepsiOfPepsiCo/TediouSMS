import RPi.GPIO as GPIO
import time

#Class that handles the keying of characters

#Based off of this graphic: https://en.wikipedia.org/wiki/Morse_code#/media/File:International_Morse_Code.svg
#Length of a "dit"
UNIT_LENGTH = 0.07 #The length of one morse code "unit"
#Length of a "dah," typically 3 times greater than the length of a "dit"
DASH_LENGTH = UNIT_LENGTH * 3 #0.21
#Length of time between parts of the same letter
LETTER_PART_SPACE_LENGTH = UNIT_LENGTH #0.07
#Length of time between different letters
LETTER_SPACE_LENGTH = UNIT_LENGTH * 3
#Length of time between words
WORD_SPACE_LENGTH = UNIT_LENGTH * 7
DOT = '.'
DASH = '-'

class TelegraphKey(object):

	#pin -> the pin the button runs to to provide output.
	def __init__(self, pin):
		self.pin = pin
		
	def key_string(self):
		while True:
			print(self.key_character())

	def key_character(self):
		character = ""
		unit = self.key_unit_positive()
		
		if unit > UNIT_LENGTH and unit < DASH_LENGTH:
			character += "."
		elif unit > DASH_LENGTH and unit < WORD_SPACE_LENGTH:
			character += "-"
			
		negative_unit = self.key_unit_negative()
			
		if negative_unit > LETTER_PART_SPACE_LENGTH and negative_unit < LETTER_SPACE_LENGTH:
			#There's not really anything to do between parts of letters
              pass
		elif negative_unit > LETTER_SPACE_LENGTH and negative_unit < WORD_SPACE_LENGTH:
			#Put a space between letters
			character += " "
		elif negative_unit > WORD_SPACE_LENGTH:
			#Put a slash to denote a space between words
			character += "/"
	
	#Key a "positive" unit - i.e. a unit coded by the user pressing then releasing the button
	#Used for everything besides unit measurements between letters and words.
	def key_unit_positive(self):
		#Hang until the button is pressed
		while not GPIO.input(self.pin):
			pass
		
		#Record the start time
		start = time.time()
		
		#Hang until button is released
		while GPIO.input(self.pin):
			pass
		
		#Return elapsed time
		return time.time() - start
		
	
	#Key a "negative" unit -- i.e. a unit that represents the space between letters or other units,
	#and is not actually part of the message. This takes place between when the button is released and
	#when it is pressed again.
	def key_unit_negative(self):
		#Record the start time
		start = time.time()
		
		#Hang until button is pushed
		while not GPIO.input(self.pin):
			pass
		
		#Return elapsed time
		return time.time() - start