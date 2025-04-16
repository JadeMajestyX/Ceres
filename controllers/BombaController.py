from controllers.Controller import Controller
import time
import threading

class BombaController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

    def automatic(self):
        self.automatico_activo = True
        def ciclo_automatico():
            while self.automatico_activo:
                self.alto()
                time.sleep(5)
                self.bajo()
                time.sleep(5)

        ciclo_automatico()
