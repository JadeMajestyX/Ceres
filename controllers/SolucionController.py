from controllers.Controller import Controller
import time
import threading

class SolucionController(Controller):
    def __init__(self, pin: int):
        super().__init__(pin)
        self._running = False
        self.thread = None

    # Función automática para administrar las soluciones en base a las semanas
    def automatic(self, semanas: int):
        if self._running:
            print("El modo automático ya está corriendo.")
            return

        self._running = True

        def run():
            print(f"Iniciando modo automático para semana {semanas}")

            # Lógica basada en las semanas del cultivo
            if semanas <= 2:
                self.activar_soluciones(a=10, b=5, c=5)
            elif 3 <= semanas <= 5:
                self.activar_soluciones(a=20, b=10, c=10)
            else:
                self.activar_soluciones(a=30, b=15, c=15)

            self._running = False

        # Ejecutar la lógica en un hilo separado para no bloquear el hilo principal
        self.thread = threading.Thread(target=run)
        self.thread.start()

    # Función para activar las soluciones
    def activar_soluciones(self, a, b, c):
        print(f"Activando soluciones: A={a}s, B={b}s, C={c}s")
        self.activar_bomba('A', a)
        self.activar_bomba('B', b)
        self.activar_bomba('C', c)

    # Función para encender una bomba durante X segundos
    def activar_bomba(self, nombre, segundos):
        print(f"Encendiendo bomba {nombre} por {segundos} segundos")
        self.alto()  # Encender la bomba usando el método del controlador padre
        time.sleep(segundos)
        self.bajo()  # Apagar la bomba
        print(f"Bomba {nombre} apagada")

    # Detener el proceso automático
    def detener(self):
        self._running = False
        print("Modo automático detenido.")
