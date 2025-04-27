import serial
import time
from models.medicionesModel import MedicionesModel
from models.alertasModel import AlertasModel
import json

# Configura el puerto serial
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=1)

# Espera a que el puerto serial esté listo
time.sleep(2)

try:
    while True:
        try:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode('utf-8').strip()
                if data:
                    mediciones = json.loads(data)
                    if 'temperature' in mediciones:
                        MedicionesModel().agregar_medicion(get_planta_id(), mediciones['temperature'], mediciones['ec'], mediciones['ph'], mediciones['water_level'])
                        AlertasModel().alerta_solucionada(get_planta_id(), "Los datos del Arduino son incorrectos")
                    else:
                        AlertasModel().agregar_alerta(get_planta_id(), "Los datos del Arduino son incorrectos")
                else:
                    print("Error: No se recibió dato válido")
        except Exception as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nLectura terminada por el usuario.")
finally:
    arduino.close()
