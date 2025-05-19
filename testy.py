import RPi.GPIO as GPIO
import time

# Configurar el modo de numeración (BCM o BOARD)
GPIO.setmode(GPIO.BCM)

# Pin GPIO al que está conectado el relé
RELE_PIN = 27  # Cambia esto según tu conexión

# Configurar el pin como salida
GPIO.setup(RELE_PIN, GPIO.OUT)

def activar_rele():
    GPIO.output(RELE_PIN, GPIO.LOW)  # LOW normalmente activa el relé
    print("Relé activado")

def desactivar_rele():
    GPIO.output(RELE_PIN, GPIO.HIGH)  # HIGH normalmente desactiva el relé
    print("Relé desactivado")

try:
    while True:
        activar_rele()
        time.sleep(0.07)
        desactivar_rele()
        time.sleep(2)

except KeyboardInterrupt:
    print("Programa detenido por el usuario")

finally:
    GPIO.cleanup()
    print("GPIO limpiado y programa finalizado")
