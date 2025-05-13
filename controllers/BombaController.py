from controllers.Controller import Controller
import time
import threading

class BombaController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

    def automatic(self, time_on: int, time_off: int):
        while True:
            self.bajo()
            time.sleep(time_on)
            self.alto()
            time.sleep(time_off)