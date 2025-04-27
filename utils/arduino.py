import serial
import time
from models.medicionesModel import MedicionesModel
from models.alertasModel import AlertasModel
import json

def leer_arduino(planta_id, tiempo_lectura):
    arduino = None
    
    while True:
        try:

            if arduino is None or not arduino.is_open:
                arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
                time.sleep(2)  # Espera a que el puerto se inicialice
                AlertasModel().alerta_solucionada(planta_id, "No se detectó el Arduino")
            
            while True:
                try:
                    time.sleep(tiempo_lectura)  # Espera antes de intentar leer el Arduino
                    if arduino.in_waiting > 0:
                        data = arduino.readline().decode('utf-8').strip()
                        if data:
                            mediciones = json.loads(data)
                            if 'temperature' in mediciones:
                                MedicionesModel().agregar_medicion(
                                    planta_id,
                                    mediciones['temperature'],
                                    mediciones['ec'],
                                    mediciones['ph'],
                                    mediciones['water_level']
                                )
                                AlertasModel().alerta_solucionada(planta_id, "Los datos del Arduino son incorrectos")
                                AlertasModel().alerta_solucionada(planta_id, "No se recibieron datos del Arduino")

                            else:
                                AlertasModel().agregar_alerta(planta_id, "Los datos del Arduino son incorrectos")
                        else:
                            AlertasModel().agregar_alerta(planta_id, "No se recibieron datos del Arduino")
                except serial.SerialException:
                    # Si ocurre un error con el puerto serial, reconectar
                    arduino.close()
                    arduino = None
                    time.sleep(2)
                    break  # Salir del ciclo para intentar reconectar

        except KeyboardInterrupt:
            break  # Salir del ciclo principal si se interrumpe

        except Exception as e:
            AlertasModel().agregar_alerta(planta_id, "No se detectó el Arduino")
            if arduino:
                arduino.close()
            time.sleep(5)

        finally:
            if arduino and arduino.is_open:
                arduino.close()
