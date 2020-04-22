import RPi.GPIO as GPIO

class State:
    def __init__(self):

        #GPIO.setwarnings(False)    # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
        self.GPIO_NO_RED = 38
        self.GPIO_NO_GREEN = 40
        GPIO.setup(self.GPIO_NO_RED, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(self.GPIO_NO_GREEN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
        
    def good(self):
        GPIO.output(self.GPIO_NO_RED, GPIO.LOW) # Turn off
        GPIO.output(self.GPIO_NO_GREEN, GPIO.HIGH) # Turn on

    def bad(self):
        GPIO.output(self.GPIO_NO_GREEN, GPIO.LOW) # Turn off
        GPIO.output(self.GPIO_NO_RED, GPIO.HIGH) # Turn on
