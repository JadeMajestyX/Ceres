from controllers.Controller import Controller
import time
import threading
import json

class PlantaController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

