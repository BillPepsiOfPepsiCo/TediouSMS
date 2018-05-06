import RPi.GPIO as GPIO
import time, pygame, numpy, asyncio
from tkinter import INSERT, END
from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
from array import array
from math import pi, sin

#Class that handles the keying of characters

#Based off of this graphic: https://en.wikipedia.org/wiki/Morse_code#/media/File:International_Morse_Code.svg
#Length of a "dit"
UNIT_LENGTH = 0.07 #The length of one morse code "unit"
#Length of a "dah," typicnumpy-1.14.3-cp27-cp27m-manylinux1_i686ally 3 times greater than the length of a "dit"
DASH_LENGTH = UNIT_LENGTH * 3 #0.21
#Length of time between parts of the same letter
LETTER_PART_SPACE_LENGTH = UNIT_LENGTH #0.07
#Length of time between different letters
LETTER_SPACE_LENGTH = UNIT_LENGTH * 3
#Length of time between words
WORD_SPACE_LENGTH = UNIT_LENGTH * 7
DOT = '.'
DASH = '-'

RECORDING = False

MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024

class TelegraphTone(pygame.mixer.Sound):

	def __init__(self, frequency):
		self.frequency = frequency
		pygame.mixer.Sound.__init__(self, buffer = self.build_samples())
		self.set_volume(1)
		
	def build_samples(self):
		period = int(round(MIXER_FREQ / self.frequency))
		amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
		samples = array("h", [0] * period)
		cur_amplitude = 0
		cur_time = 0
		
		for i in range(period):
			omega = 2 * pi * self.frequency
			delta_t = 1 / self.frequency / period
			cur_time += delta_t
			cur_amplitude = amplitude * sin(omega * cur_time)
			samples[i] = int(cur_amplitude)
		
		return samples
		
class TelegraphKey(object):

	def __init__(self, input_pin, signal_pin, recording_indicator_pin, incoming_message_indicator_pin, output_widget):
		self.input_pin = input_pin
		self.signal_pin = signal_pin
		self.recording_indicator_pin = recording_indicator_pin
		self.incoming_message_indicator_pin = incoming_message_indicator_pin
		self.output_widget = output_widget
		
		self.setup_gpio()
		
		self._750_Hz_tone = None
		self._keyed_string = None
		self.__run = True
		
		self.init_sounds()
		self._thread = Thread(target = self.poll_loop, daemon = True)
		self._thread.start()
        
	"""
	Sets up the GPIO pins passed to the constructor.
	Also sets the pin numbering sceme to Broadcom mode.
	"""
	def setup_gpio(self):
		print("Setting GPIO mode to Broadcom Pin Mode")
		GPIO.setmode(GPIO.BCM)
		
		for pin in (self.signal_pin, self.input_pin):
			GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
			
		for pin in (self.recording_indicator_pin, self.incoming_message_indicator_pin):
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, GPIO.LOW)
	
	def __deinit(self):
		RECORDING = False
		self.__run = False
		GPIO.cleanup()
		
	def poll_loop(self):
		while self.__run:
			self.poll_and_toggle_recording()

	"""
	Runs on the _listener_thread when this class is initialized.
	Toggles the global RECORDING variable based on if a button press was detected.
	"""
	def poll_and_toggle_recording(self):
		global RECORDING
		#I know what you're thinking: jesus bro, a global async variable.
		#But keep in mind: this is only being written to from inside
		#one thread, and is only read until the button is pressed again
		#(the update of which occurs in the same thread as all other
		#writes). So, it's surprisingly threadsafe.
	
		while True:
			#Listen for a high voltage on the signal pin
			#Begin keying the input until the signal pin recieves another high voltage
			button_pressed = GPIO.input(self.signal_pin)
			if button_pressed:
				print("RECORDING STATE CHANGED TO =>", bool(button_pressed))
				RECORDING = not RECORDING
				GPIO.output(self.recording_indicator_pin, RECORDING)
				break
		
		if RECORDING:
			self.output_widget.delete('1.0', END)
			pool = ThreadPool(processes = 1)
			self._keyed_string = pool.apply_async(self.key_string)
		else:
			self.output_widget.configure(state = "normal")
			self.output_widget.insert('1.0', self._keyed_string.get())
			self.output_widget.configure(state = "disabled")
		
		sleep(0.2)

	"""
	Call this method to initialize the 750 Hz tone and play it when the button's pressed.
	Without calling this the button will not play a sound.
	"""
	def init_sounds(self):
		pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS, MIXER_BUFF)
		pygame.init()
		self._750_Hz_tone = TelegraphTone(750)

	"""
	Begins keying a string. Returns the string when the
	signal pin button is pressed.
	"""
	def key_string(self):
		string = ""

		while RECORDING:
			string += self.key_character()

		return string
		

	def key_character(self):
		character = ""
			
		unit = self.key_unit_positive()

		if unit > UNIT_LENGTH and unit < DASH_LENGTH:
			character += "."
			#TODO: play "dit" sound from speaker
		elif unit > DASH_LENGTH and unit < WORD_SPACE_LENGTH:
			character += "-"
			#TODO: play "dah" sound from speaker
			
		negative_unit = self.key_unit_negative()
			
		if negative_unit > LETTER_PART_SPACE_LENGTH and negative_unit < LETTER_SPACE_LENGTH:
			#There's not really anything to do between parts of letters
			pass
		elif negative_unit > LETTER_SPACE_LENGTH and negative_unit < WORD_SPACE_LENGTH:
			#Put a space between letters
			character += " "
		elif negative_unit > WORD_SPACE_LENGTH:
			#Put a slash to denote a space between words
			character += " / "

		return character
	
	#Key a "positive" unit - i.e. a unit coded by the user pressing then releasing the button
	#Used for everything besides unit measurements between letters and words.
	def key_unit_positive(self):
		#Hang until the button is pressed
		while not GPIO.input(self.input_pin) and RECORDING:
			pass
		
		#Record the start time
		self._750_Hz_tone.play(-1)
		start = time.time()
		
		#Hang until button is released
		while GPIO.input(self.input_pin) and RECORDING:
			pass
		
		self._750_Hz_tone.stop()
		#Return elapsed time
		return time.time() - start
		
	
	#Key a "negative" unit -- i.e. a unit that represents the space between letters or other units,
	#and is not actually part of the message. This takes place between when the button is released and
	#when it is pressed again.
	def key_unit_negative(self):
		#Record the start time
		start = time.time()
		
		#Hang until button is pushed
		while not GPIO.input(self.input_pin) and RECORDING:
			pass
		
		#Return elapsed time
		return time.time() - start
