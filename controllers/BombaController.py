from controllers.Controller import Controller
import time
import threading
from utils.functions.functions import status

class BombaController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

    def automatic(self, time_on: int, time_off: int):
        status_bomb = status("bomba")
        while True:
            if status_bomb == "True":
                self.alto()
                time.sleep(time_on)
                self.bajo()
                time.sleep(time_off)
            else:
                self.alto()
                time.sleep(1)