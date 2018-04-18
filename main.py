import RPi.GPIO as GPIO
from Telegraph import TelegraphKey

PIN = 17

if __name__ == "__main__":
    #Enter broadcom pin numbering mode
    GPIO.setmode(GPIO.BCM)
    
    #Setting the default to PUD_DOWN makes the button default to an off
    #position, programatically.
    GPIO.setup(PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    key = TelegraphKey(PIN)
    
    while True:
        key.key_string()
	