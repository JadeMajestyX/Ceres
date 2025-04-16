import json
import time
import threading
from controllers.BombaController import BombaController
from controllers.PhController import PhController

CONFIG_PATH = "utils/config.json"

def get_tiempo(actuador_nombre: str) -> float:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["actuadores"][actuador_nombre]["tiempo_activacion_segundos"]

def status(actuador_nombre: str) -> bool:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["actuadores"][actuador_nombre]["status"]

def start_automatic(ctrl, actuador_nombre):
    def ciclo():
        while True:
            stats = status(actuador_nombre)
            ph = 8.0  # Placeholder for actual pH value

            if stats == "True" and actuador_nombre == "bomba" or stats == "True" and actuador_nombre == "ph" and ph < 7.0 or stats == "True" and actuador_nombre == "phless" and ph > 7.0:
                tiempo = get_tiempo(actuador_nombre)
                ctrl.alto()
                time.sleep(tiempo)
                ctrl.bajo()
                time.sleep(tiempo)
            elif(actuador_nombre != "bomba" and stats == "False"):
                ctrl.bajo()
                time.sleep(1)
            else:
                ctrl.alto()
                time.sleep(1)
    thread = threading.Thread(target=ciclo, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    # Inicialización de controladores
    bomba    = BombaController(pin=17)
    ph       = PhController(pin=27)
    phless   = PhController(pin=22)

    # Arranca los hilos, indicando el nombre que coincide con las claves del JSON
    hilo_bomba  = start_automatic(bomba,  "bomba")
    hilo_ph     = start_automatic(ph,     "ph")
    hilo_phless = start_automatic(phless, "phless")

    try:
        # Hilo principal en espera para mantener vivo el programa
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bomba.cleanup()
        ph.cleanup()
        phless.cleanup()
