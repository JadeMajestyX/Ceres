from controllers.Controller import Controller
import time
from utils.functions.functions import get_tiempo_sensores, get_planta_id, status
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel
from datetime import datetime

class PhController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        self.alto()
        
    def automatic(self, time_on: int):
        while True:
            status_ph = status("ph")
            if status_ph == "True":
                planta_id = get_planta_id()
                tiempo_medicion = MedicionesModel().obtener_medicion(planta_id, "time")  # Puede ser str o datetime
                id = MedicionesModel().obtener_medicion(get_planta_id(), "id")
                ph = MedicionesModel().obtener_medicion(get_planta_id(), "ph")
                phmin = parametrosModel().obtener_parametro(get_planta_id(), "phmin")
                wait = get_tiempo_sensores()
                if isinstance(tiempo_medicion, str):
                    tiempo_medicion = datetime.strptime(tiempo_medicion, "%Y-%m-%d %H:%M:%S")

                ahora = datetime.now()
                diferencia = (ahora - tiempo_medicion).total_seconds()
                if diferencia < 1:
                    print("time_up")
                    if ph < phmin:
                        print("prueba up")
                        self.bajo()
                        ActuadoresModel().agregar_accion(id, "ph", "alto")
                        time.sleep(0.5)
                        ActuadoresModel().agregar_accion(id, "ph", "bajo")
                        self.alto()
                        time.sleep(0.25)
                    else:
                        self.alto()
                        time.sleep(0.25)
            else:
                self.alto()
                time.sleep(0.25)

class PhlessController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        self.alto()
        
    def automatic(self, time_on: int):
        while True:
            
            stats = status("ph")
            if stats == "True":
                planta_id = get_planta_id()
                tiempo_medicion = MedicionesModel().obtener_medicion(planta_id, "time")  # Puede ser str o datetime
                id = MedicionesModel().obtener_medicion(get_planta_id(), "id")
                ph = MedicionesModel().obtener_medicion(get_planta_id(), "ph")
                phmax = parametrosModel().obtener_parametro(get_planta_id(), "phmax")
                wait = get_tiempo_sensores()
                    

                if isinstance(tiempo_medicion, str):
                        
                    tiempo_medicion = datetime.strptime(tiempo_medicion, "%Y-%m-%d %H:%M:%S")

                ahora = datetime.now()
                diferencia = (ahora - tiempo_medicion).total_seconds()
                print(phmax)

                if diferencia < 1:
                    if ph > phmax:
                        self.bajo()
                        print("prueba down")
                        ActuadoresModel().agregar_accion(id, "phless", "activo")
                        time.sleep(0.5)
                        ActuadoresModel().agregar_accion(id, "phless", "inactivo")
                        self.alto()
                        time.sleep(0.25)
                    else:
                        print("no")
                        self.alto()
                        time.sleep(0.25)
            else:
                self.alto()
                time.sleep(0.25)





