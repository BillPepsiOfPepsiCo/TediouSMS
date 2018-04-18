import RPi.GPIO as GPIO
import time

PIN = 17
DIT_LENGTH = 0.07
DAH_LENGTH = DIT_LENGTH * 3 #0.21

#Returns the length of time for which the button was pressed
def listen():
    
    while not GPIO.input(PIN):
        pass
    
    start = time.time()
    
    while GPIO.input(PIN):
        pass
    
    return time.time() - start        

if __name__ == "__main__":
    #Enter broadcom pin numbering mode
    GPIO.setmode(GPIO.BCM)
    
    #Setting the default to PUD_DOWN makes the button default to an off
    #position, programatically.
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    while True:
        print(listen())
	