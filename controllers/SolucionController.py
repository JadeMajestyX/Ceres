from controllers.Controller import Controller
from utils.functions.functions import get_tiempo_sensores, get_planta_id, get_pin, tiempo
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel
import time
import threading
from datetime import datetime

class SolucionController1(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        self.alto()

class SolucionController2(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        self.alto()

class SolucionController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        # Instancia una sola vez los controladores secundarios
        self.solucion2 = SolucionController2(get_pin("solucion", "pin2"))
        self.solucion3 = SolucionController1(get_pin("solucion", "pin3"))
        self._running = False
        self.alto()

    def activar_con_pulso(self, controlador, tiempo):
        controlador.bajo()
        time.sleep(tiempo)
        controlador.alto()

    def automatic(self, time_on: int):
        self._running = True

        while self._running:
            try:
                planta_id = get_planta_id()
                tiempo_medicion = MedicionesModel().obtener_medicion(planta_id, "time")  # Puede ser str o datetime
                print(f"Tiempo de medición: {tiempo_medicion}")
                id_medicion = MedicionesModel().obtener_medicion(planta_id, "id")
                ec = MedicionesModel().obtener_medicion(planta_id, "ec")
                ecmin = parametrosModel().obtener_parametro(planta_id, "ecmin")
                ecmax = parametrosModel().obtener_parametro(planta_id, "ecmax")
                wait = get_tiempo_sensores()

                # Convertir a datetime si es string
                if isinstance(tiempo_medicion, str):
                    tiempo_medicion = datetime.strptime(tiempo_medicion, "%Y-%m-%d %H:%M:%S")

                ahora = datetime.now()
                diferencia = (ahora - tiempo_medicion).total_seconds()

                if diferencia < 10:  # Solo si la medición es reciente (<10 segundos)
                    if ec < ecmin:
                        self.activar_con_pulso(self, 2.5)
                        ActuadoresModel().agregar_accion(id_medicion, "solucion", "activo")
                        self.activar_con_pulso(self.solucion2, 5)
                        self.activar_con_pulso(self.solucion3, 2.5)

                time.sleep(wait)
            except Exception as e:
                print(f"Error en automatic(): {e}")
                time.sleep(5)

        
    def stop(self):
        self._running = False
