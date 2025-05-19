from controllers.Controller import Controller
import time
from utils.functions.functions import get_tiempo_sensores, get_planta_id
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel

class PhController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        
    def automatic(self, time_on: int):
        while True:
            id = MedicionesModel().obtener_medicion(get_planta_id(), "id")
            ph = MedicionesModel().obtener_medicion(get_planta_id(), "ph")
            phmin = parametrosModel().obtener_parametro(get_planta_id(), "phmin")
            wait = get_tiempo_sensores()

            if ph < phmin:
                self.bajo()
                ActuadoresModel().agregar_accion(id, "ph", "alto")
                time.sleep(time_on)
                ActuadoresModel().agregar_accion(id, "ph", "bajo")
                self.alto()
                time.sleep(wait)
            else:
                self.alto()
                time.sleep(wait)

class PhlessController(Controller):
    def automatic(self, time_on: int):
        while True:
            id = MedicionesModel().obtener_medicion(get_planta_id(), "id")
            ph = MedicionesModel().obtener_medicion(get_planta_id(), "ph")
            phmax = parametrosModel().obtener_parametro(get_planta_id(), "phmax")
            wait = get_tiempo_sensores()

            if ph > phmax:
                self.bajo()
                ActuadoresModel().agregar_accion(id, "phless", "activo")
                time.sleep(time_on)
                ActuadoresModel().agregar_accion(id, "phless", "inactivo")
                self.alto()
                time.sleep(wait)
            else:
                self.alto()
                time.sleep(wait)





