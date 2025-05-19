from controllers.Controller import Controller
from utils.functions.functions import get_tiempo_sensores, get_planta_id, get_pin
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel
import time
import threading

class SolucionController1(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

class SolucionController2(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)

class SolucionController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        # Instancia una sola vez los controladores secundarios
        self.solucion2 = SolucionController2(get_pin("solucion", "pin2"))
        self.solucion3 = SolucionController1(get_pin("solucion", "pin3"))
        self._running = False

    def activar_con_pulso(self, controlador, tiempo):
        controlador.alto()
        time.sleep(tiempo)
        controlador.bajo()

    def automatic(self, time_on: int):
        self._running = True
        
        while self._running:
            try:
                planta_id = get_planta_id()
                id_medicion = MedicionesModel().obtener_medicion(planta_id, "id")
                ec = MedicionesModel().obtener_medicion(planta_id, "ec")
                ecmin = parametrosModel().obtener_parametro(planta_id, "ecmin")
                ecmax = parametrosModel().obtener_parametro(planta_id, "ecmax")
                wait = get_tiempo_sensores()

                if ec < ecmin:
                    self.activar_con_pulso(self, time_on)
                    ActuadoresModel().agregar_accion(id_medicion, "solucion", "activo")
                    self.activar_con_pulso(self.solucion2, time_on)
                    self.activar_con_pulso(self.solucion3, time_on)

                time.sleep(wait)
            except Exception as e:
                print(f"Error en automatic(): {e}")
                time.sleep(5)  # Evita bucle rápido en caso de errores

    def stop(self):
        self._running = False
