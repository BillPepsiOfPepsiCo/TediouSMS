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

	def key_character(self):
		unit = self.key_unit()
		
		if unit > UNIT_LENGTH and unit < DASH_LENGTH:
			print("DIT")
		elif unit > DASH_LENGTH and unit < WORD_SPACE_LENGTH:
			print("DAH")
		elif unit > WORD_SPACE_LENGTH:
			print("--- (new word) ---")
	
	#The base function for keying in a character
	def key_unit(self):
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