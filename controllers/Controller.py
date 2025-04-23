import RPi.GPIO as GPIO
 
class Controller():
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def alto(self): # Set pin to HIGH
        GPIO.output(self.pin, GPIO.HIGH)

    def bajo(self): # Set pin to LOW
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self): # Cleanup GPIO settings
        GPIO.cleanup()