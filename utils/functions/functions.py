from models.medicionesModel import MedicionesModel
from models.plantasModel import PlantasModel
from models.alertasModel import AlertasModel
import json
import time
import datetime

def get_planta_id():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["planta"]["id"]

def get_nombre_planta():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    id = data["planta"]["id"]
    planta = PlantasModel().get_planta_id(id)
    if planta:
        return planta['nombre']
    

def get_status_actuador(tipo):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["actuadores"][tipo]["status"]

def update_status_actuador(tipo, status):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["actuadores"][tipo]["status"] = status
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def upadate_tiempo_bomba(tiempo_bomba):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["actuadores"]["bomba"]["time_off"] = tiempo_bomba
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def update_tiempo_bomba_on(tiempo_bomba_on):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["actuadores"]["bomba"]["time_on1"] = tiempo_bomba_on
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def update_tiempo_lectura(tiempo_lectura):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["sensores"]["tiempo_lectura"] = tiempo_lectura
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def tiempo():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    dia = data["planta"]["time"]
    dia_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    #retornar el tiempo en dias desde la fecha de inicio
    return (datetime.datetime.strptime(dia_actual, "%Y-%m-%d") - datetime.datetime.strptime(dia, "%Y-%m-%d")).days


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
    

def get_dato_planta(planta_id, dato):
    try:
        planta = PlantasModel().obtener_planta(planta_id)
        if planta:
            if dato == "nombre":
                AlertasModel().alerta_solucionada(planta_id, "No se pudo obtener el dato de la planta")
                return planta[1]
            elif dato == "descripcion":
                AlertasModel().alerta_solucionada(planta_id, "No se pudo obtener el dato de la planta")
                return planta[2]
            else:
                raise ValueError("Dato no válido")
    except Exception as e:
        AlertasModel().agregar_alerta(planta_id, "No se pudo obtener el dato de la planta")
        return None
    
def get_tiempo_sensores():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["sensores"]["tiempo_lectura"]

def get_pin(tipo, pin):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["actuadores"][tipo][pin]

def get_tiempo_encendido(tipo, number=1):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["actuadores"][tipo][f"time_on{number}"]
def get_tiempo_apagado(tipo):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["actuadores"][tipo]["time_off"]

def status(tipo):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["actuadores"][tipo]["status"]

def update_tiempo_lectura(tiempo_lectura):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["sensores"]["tiempo_lectura"] = tiempo_lectura
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)


def update_planta(id_planta):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["planta"]["id"] = id_planta
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def update_tiempo_lectura(tiempo):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["sensores"]["tiempo_lectura"] = tiempo
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def update_email(email):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["email"]['email'] = email
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def update_password(password):
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    data["password"] = password
    with open("utils/config.json", "w") as f:
        json.dump(data, f, indent=4)

def get_email():
    with open("utils/config.json", "r") as f:
        data = json.load(f)
    return data["email"]["email"]