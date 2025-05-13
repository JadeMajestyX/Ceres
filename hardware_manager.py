import json
import time
import serial
from controllers.BombaController import BombaController
from controllers.PhController import PhController, PhlessController
from controllers.SolucionController import SolucionController
from models.parametrosModel import parametrosModel
import threading
from utils.arduino import leer_arduino
from models.alertasModel import AlertasModel
from models.medicionesModel import MedicionesModel
from utils.functions.functions import get_agua_maximo, get_agua_minimo, nivel_de_agua
from utils.functions.functions import get_email
from utils.raspberry import Raspberry

CONFIG_PATH = "utils/config.json"


# === FUNCIONES JSON DE CONFIG ===
def get_planta_id():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["planta"]["id"]

def get_tiempo_sensores():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["sensores"]["tiempo_lectura"]


def status(actuador_nombre: str) -> bool:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data["actuadores"][actuador_nombre]["status"]

def main():
    planta_id = get_planta_id()

    # Pasar planta_id al hilo
    hilo_arduino = threading.Thread(target=leer_arduino, args=(planta_id, get_tiempo_sensores()), daemon=True)
    hilo_arduino.start()

    hilo_bomba = threading.Thread(target=Raspberry().bomba_automatic, daemon=True)
    hilo_bomba.start()

    hilo_solucion = threading.Thread(target=Raspberry().solucion_automatic, daemon=True)
    hilo_solucion.start()

    while True:

        # === BASE DE DATOS ===
        parametros = parametrosModel().obtener_parametros(get_planta_id())

        temp_min = parametros[0][2]
        temp_max = parametros[0][3]
        ph_min = parametros[0][4]
        ph_max = parametros[0][5]
        ec_min = parametros[0][6]
        ec_max = parametros[0][7]

        # === JSON DE CONFIG ===
        emails = get_email()

        # Asigna a variables
        email1 = emails['email1']
        email2 = emails['email2']
        email3 = emails['email3']
        
        # if email1 != "":
        #     EmailController().enviar_email(email1, "Alerta de la planta", "Se ha detectado un problema en la planta")
        # if email2 != "":
        #     EmailController().enviar_email(email2, "Alerta de la planta", "Se ha detectado un problema en la planta")
        # if email3 != "":
        #     EmailController().enviar_email(email3, "Alerta de la planta", "Se ha detectado un problema en la planta")



        #medicione
        medicion = MedicionesModel().obtener_mediciones(planta_id)

        if medicion:
            id = medicion[0]
            temp_value = medicion[2]
            ph_value = medicion[3]
            ec_value = medicion[4]
            water_value = medicion[5]

            # === ALERTAS ===
            #ph
            if ph_value > ph_max and ph_value < ph_max + 1.2:
                AlertasModel().agregar_alerta(planta_id, "El pH es alto", id)
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado altos")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado bajos")
                AlertasModel().alerta_solucionada(planta_id, "El pH es bajo")
            if ph_value < ph_min and ph_value > ph_min - 1.2:
                AlertasModel().agregar_alerta(planta_id, "El pH es bajo", id)
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado bajos")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado altos")
                AlertasModel().alerta_solucionada(planta_id, "El pH es alto")

            if ph_value > ph_max+1.2:
                AlertasModel().agregar_alerta(planta_id, "Los niveles de pH son demasiado altos", id)
                AlertasModel().alerta_solucionada(planta_id, "El pH es alto")
                AlertasModel().alerta_solucionada(planta_id, "El pH es bajo")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado bajos")
            if ph_value < ph_min-1.2:
                AlertasModel().agregar_alerta(planta_id, "Los niveles de pH son demasiado bajos", id)
                AlertasModel().alerta_solucionada(planta_id, "El pH es bajo")
                AlertasModel().alerta_solucionada(planta_id, "El pH es alto")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado altos")
            if ph_value > ph_min and ph_value < ph_max:
                AlertasModel().alerta_solucionada(planta_id, "El pH es alto")
                AlertasModel().alerta_solucionada(planta_id, "El pH es bajo")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado altos")
                AlertasModel().alerta_solucionada(planta_id, "Los niveles de pH son demasiado bajos")

            #temperatura
            if temp_value > temp_max and temp_value < temp_max + 5:
                AlertasModel().agregar_alerta(planta_id, "La temperatura del agua es alta", id)
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es baja")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado baja")
            if temp_value < temp_min and temp_value > temp_min - 5:
                AlertasModel().agregar_alerta(planta_id, "La temperatura del agua es baja", id)
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado baja")
            if temp_value > temp_max+5:
                AlertasModel().agregar_alerta(planta_id, "La temperatura del agua es demasiado alta", id)
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es baja")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado baja")
            if temp_value < temp_min-5:
                AlertasModel().agregar_alerta(planta_id, "La temperatura del agua es demasiado baja", id)
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es baja")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado alta")
            if temp_value > temp_min and temp_value < temp_max:
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es baja")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La temperatura del agua es demasiado baja")

            #conductividad
            if ec_value > ec_max and ec_value < ec_max + 1:
                AlertasModel().agregar_alerta(planta_id, "La conductividad es alta", id)
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es baja")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado baja")
            if ec_value < ec_min and ec_value > ec_min - 1:
                AlertasModel().agregar_alerta(planta_id, "La conductividad es baja", id)
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado baja")
            if ec_value > ec_max+1:
                AlertasModel().agregar_alerta(planta_id, "La conductividad es demasiado alta", id)
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es baja")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado baja")
            if ec_value < ec_min-1:
                AlertasModel().agregar_alerta(planta_id, "La conductividad es demasiado baja", id)
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es baja")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado alta")
            if ec_value > ec_min and ec_value < ec_max:
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es baja")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado alta")
                AlertasModel().alerta_solucionada(planta_id, "La conductividad es demasiado baja")

            nivel = nivel_de_agua(planta_id)

            if nivel <= 0:
                AlertasModel().agregar_alerta(planta_id, "No hay agua", id)
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es bajo")
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es alto")
            elif 0 < nivel < 30:
                AlertasModel().agregar_alerta(planta_id, "El nivel de agua es bajo", id)
                AlertasModel().alerta_solucionada(planta_id, "No hay agua")
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es alto")
            elif nivel > 100:
                AlertasModel().agregar_alerta(planta_id, "El nivel de agua es alto", id)
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es bajo")
                AlertasModel().alerta_solucionada(planta_id, "No hay agua")
            else:
                AlertasModel().alerta_solucionada(planta_id, "No hay agua")
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es bajo")
                AlertasModel().alerta_solucionada(planta_id, "El nivel de agua es alto")



if __name__ == "__main__":
    main()
