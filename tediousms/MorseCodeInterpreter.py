"""
So this file is actually unused.
This is due to the fact that we are
not skilled morse code typists
and testing would be very difficult 
if we tried to key actual letters instead
of just little test strings.
"""

ASCII_TABLE = {
	'A' : ".-",
	'B' : "-...",
	'C' : "-.-.",
	'D' : "-..",
	'E' : ".",
	'F' : "..-.",
	'G' : "--.",
	'H' : "....",
	'I' : "..",
	'J' : ".---",
	'K' : "-.-",
	'L' : ".-..",
	'M' : "--",
	'N' : "-.",
	'O' : "---",
	'P' : ".--.",
	'Q' : "--.-",
	'R' : ".-.",
	'S' : "...",
	'T' : "-",
	'U' : "..-",
	'V' : "...-",
	'W' : ".--",
	'X' : "-..-",
	'Y' : "-.--",
	'Z' : "--..",
	
	'1' : ".----",
	'2' : "..---",
	'3' : "...--",
	'4' : "....-",
	'5' : ".....",
	'6' : "-....",
	'7' : "--...",
	'8' : "---..",
	'9' : "----.",
	'0' : "-----",
	
	' ' : '/'
}

MORSE_CODE_TABLE = {v : k for k, v in ASCII_TABLE.items()}

def is_morse_code(str):
	#Checks to see if it's morse code by filtering away all valid characters and checking the length.
	return len(filter(lambda s: s not in ['-', ' ', '.', '/'], str)) == 0
	
def is_ascii(str):
	return not is_morse_code(str)

def convert_to_morse_code(str):
	if is_morse_code(str):
		return str
	
	morse_string = ''
	
	for c in str.upper():
		morse_string += ASCII_TABLE[c] + " "
		
	return morse_string.rstrip()

def convert_to_ascii(str):
	if is_ascii(str):
		return str
	
	ascii_string = ''
	
	for morse_term in str.split(' '):
		ascii_string += MORSE_CODE_TABLE[morse_term]
		
	return ascii_string