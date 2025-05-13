from controllers.BombaController import BombaController
from utils.functions.functions import status, get_tiempo_encendido, get_tiempo_apagado, get_pin
import time
from models.medicionesModel import MedicionesModel
from models.parametrosModel import parametrosModel
from controllers.PhController import PhController, PhlessController
from controllers.SolucionController import SolucionController

class Raspberry:
    def __init__(self):
        self.bomba = BombaController(get_pin("bomba", "pin1"))
        self.ph = PhController(get_pin("ph", "pin1"))
        self.phless = PhlessController(get_pin("ph", "pin2"))
        self.solucion = SolucionController(get_pin("solucion", "pin1"))

    def bomba_automatic(self):
        status_bomb = status("bomba")
        time_off = get_tiempo_apagado("bomba")
        time_on = get_tiempo_encendido("bomba")
        if status_bomb:
            self.bomba.automatic(time_on, time_off)
        else:
            self.bomba.alto()

    def ph_automatic(self):
        status_ph= status("ph")
        ph_time_on = get_tiempo_encendido("ph")
        if status_ph:
            self.ph.automatic(ph_time_on)
        else:
            self.ph.bajo()

    def solucion_automatic(self):
        status_solucion = status("solucion")
        time_on = get_tiempo_encendido("solucion")
        if status_solucion:
            self.solucion.automatic(time_on)
        else:
            self.solucion.bajo()