import json
import time
from controllers.BombaController import BombaController
from controllers.PhController import PhController
from models.parametrosModel import parametrosModel

CONFIG_PATH = "utils/config.json"

#datos de json
def get_planta_id():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["planta"]["id"]

def get_tiempo(actuador_nombre: str) -> float:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["actuadores"][actuador_nombre]["tiempo_activacion_segundos"]

def status(actuador_nombre: str) -> bool:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["actuadores"][actuador_nombre]["status"]


#database
parametros = parametrosModel().obtener_parametros(get_planta_id())

temp_min = parametros[0][2]
temp_max = parametros[0][3]
ph_min = parametros[0][4]
ph_max = parametros[0][5]
ec_min = parametros[0][6]
ec_max = parametros[0][7]

print(temp_min)