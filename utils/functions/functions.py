from models.medicionesModel import MedicionesModel
import json

def get_planta_id():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["planta"]["id"]

def get_agua_maximo():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["sensores"]["nivel_agua"]["valor_maximo"]

def get_agua_minimo():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["sensores"]["nivel_agua"]["valor_minimo"]

def nivel_de_agua(planta_id):
    try:
        medicion = MedicionesModel().obtener_medicion(planta_id, "water")
        if medicion > 0:
            porcentaje = (medicion / get_agua_maximo()) * 100
            return porcentaje
        else:
            return 0
    except Exception as e:
        return 0
    
