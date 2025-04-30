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

def get_email():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["email"]

def nivel_de_agua(planta_id):
    try:
        medicion   = MedicionesModel().obtener_medicion(planta_id, "water")
        dist_vacio = get_agua_minimo()   # distancia sensor ↔ agua con tanque vacío
        dist_lleno = get_agua_maximo()   # distancia sensor ↔ agua con tanque lleno

        rango = dist_vacio - dist_lleno
        if rango <= 0:
            # configuración inválida: get_agua_minimo() debe ser > get_agua_maximo()
            return 0.0

        porcentaje = ((dist_vacio - medicion) / rango) * 100

        # forzamos sólo el mínimo a 0, permitiendo >100
        porcentaje = max(0.0, porcentaje)

        return porcentaje

    except Exception:
        # ante cualquier error devolvemos 0 %
        return 0.0
