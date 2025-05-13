from controllers.Controller import Controller
import time
import threading
from utils.functions.functions import get_tiempo_sensores, get_planta_id
from models.parametrosModel import parametrosModel
from models.medicionesModel import MedicionesModel
from models.actuadoresModel import ActuadoresModel

class PhlessController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        


