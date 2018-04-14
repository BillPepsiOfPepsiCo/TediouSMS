from MorseCodeInterpreter import *

#UNIT TEST!
if __name__ == "__main__":
	STRING = "COLLIN MOM GAY SEND HELP"
	STRING2 = convert_to_morse_code(STRING)
	STRING3 = convert_to_ascii(STRING2)
	
	assert STRING == "COLLIN MOM GAY SEND HELP"
	assert STRING2 == "-.-. --- .-.. .-.. .. -. / -- --- -- / --. .- -.-- / ... . -. -.. / .... . .-.. .--. "
	assert STRING3 == "COLLIN MOM GAY SEND HELP"