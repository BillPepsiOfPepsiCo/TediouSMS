import RPi.GPIO as GPIO
import time

PIN = 17
DIT_LENGTH = 0
DAH_LENGTH = DIT_LENGTH * 3

if __name__ == "__main__":
    #Enter broadcom pin numbering mode
    GPIO.setmode(GPIO.BCM)
    
    #Setting the default to PUD_DOWN makes the button default to an off
    #position, programatically.
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    GPIO.add_event_detect(PIN, GPIO.BOTH, callback = thick_callback, bouncetime = 200)

def listen():
    
    
            
            
	