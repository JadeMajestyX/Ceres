from controllers.Controller import Controller
import time
from utils.functions.functions import get_tiempo_sensores, get_planta_id
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel
from datetime import datetime

class PhController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        
    def automatic(self, time_on: int):
        while True:
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
            if diferencia < 10:
                if ph < phmin:
                    self.bajo()
                    ActuadoresModel().agregar_accion(id, "ph", "alto")
                    time.sleep(0.5)
                    ActuadoresModel().agregar_accion(id, "ph", "bajo")
                    self.alto()
                    time.sleep(wait)
                else:
                    self.alto()
                    time.sleep(wait)

class PhlessController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        
    def automatic(self, time_on: int):
        while True:
            
            try:
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

                if diferencia < 15:
                    if ph > phmax:
                        self.bajo()
                        print("hola")
                        ActuadoresModel().agregar_accion(id, "phless", "activo")
                        time.sleep(0.5)
                        ActuadoresModel().agregar_accion(id, "phless", "inactivo")
                        self.alto()
                        time.sleep(wait)
                    else:
                        print("no")
                        self.alto()
                        time.sleep(wait)
            except Exception as e:
                print(f"Error en PhlessController: {e}")
                time.sleep(5)





