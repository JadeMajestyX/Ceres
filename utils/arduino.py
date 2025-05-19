import serial
import time
from models.medicionesModel import MedicionesModel
from models.alertasModel import AlertasModel
import json

def leer_arduino(planta_id, tiempo_lectura):
    arduino = None

    def leer_ultima_linea(arduino):
        ultima_linea = None
        start_time = time.time()
        while (time.time() - start_time) < 2:
            while arduino.in_waiting > 0:
                ultima_linea = arduino.readline().decode('utf-8').strip()
            time.sleep(0.05)
        return ultima_linea

    while True:
        try:
            if arduino is None or not arduino.is_open:
                try:
                    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
                except serial.SerialException:
                    print("No se detectó el puerto")
                    AlertasModel().agregar_alerta(planta_id, "No se detectó el Arduino")
                    time.sleep(5)
                    continue

                time.sleep(4)
                arduino.reset_input_buffer()
                AlertasModel().alerta_solucionada(planta_id, "No se detectó el Arduino")

                arduino.write(b'S')
                time.sleep(0.5)
                data = leer_ultima_linea(arduino)

                if data:
                    try:
                        mediciones = json.loads(data)
                        if 'temperature' in mediciones:
                            MedicionesModel().agregar_medicion(
                                planta_id,
                                mediciones['temperature'],
                                mediciones['ph'],
                                mediciones['ec'],
                                mediciones['water_level']
                            )
                            AlertasModel().alerta_solucionada(planta_id, "Los datos del Arduino son incorrectos")
                            AlertasModel().alerta_solucionada(planta_id, "No se recibieron datos del Arduino")
                        else:
                            AlertasModel().agregar_alerta(planta_id, "Los datos del Arduino son incorrectos")
                    except json.JSONDecodeError:
                        AlertasModel().agregar_alerta(planta_id, "Los datos del Arduino no tienen formato JSON")
                else:
                    AlertasModel().agregar_alerta(planta_id, "No se recibieron datos del Arduino")

            while True:
                try:
                    time.sleep(tiempo_lectura)
                    arduino.write(b'S')
                    time.sleep(0.5)
                    data = leer_ultima_linea(arduino)

                    if data:
                        try:
                            mediciones = json.loads(data)
                            if 'temperature' in mediciones:
                                MedicionesModel().agregar_medicion(
                                    planta_id,
                                    mediciones['temperature'],
                                    mediciones['ph'],
                                    mediciones['ec'],
                                    mediciones['water_level']
                                )
                                AlertasModel().alerta_solucionada(planta_id, "Los datos del Arduino son incorrectos")
                                AlertasModel().alerta_solucionada(planta_id, "No se recibieron datos del Arduino")
                            else:
                                AlertasModel().agregar_alerta(planta_id, "Los datos del Arduino son incorrectos")
                        except json.JSONDecodeError:
                            AlertasModel().agregar_alerta(planta_id, "Los datos del Arduino no tienen formato JSON")
                    else:
                        AlertasModel().agregar_alerta(planta_id, "No se recibieron datos del Arduino")

                except serial.SerialException:
                    if arduino:
                        arduino.close()
                    arduino = None
                    time.sleep(2)
                    break

        except KeyboardInterrupt:
            break

        except Exception as e:
            AlertasModel().agregar_alerta(planta_id, f"Error inesperado: {str(e)}")
            if arduino:
                arduino.close()
            time.sleep(5)

        finally:
            if arduino and arduino.is_open:
                arduino.close()
