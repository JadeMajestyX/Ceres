from models.Model import Model

class ActuadoresModel(Model):
    def __init__(self):
        super().__init__()

    def obtener_mediciones(self, planta_id):
        try:
            self.cursor.execute("SELECT * FROM mediciones WHERE planta_id = %s ORDER BY id DESC LIMIT 1", (planta_id,))
            return self.cursor.fetchone()
        finally:
            self.close()

    def agregar_accion(self, medicion_id, nombre, accion):
        try:
            self.cursor.execute(
                "INSERT INTO actuadores (medicion_id, nombre, accion) VALUES (%s,%s,%s)",
                (medicion_id, nombre, accion)
            )
            self.connection.commit()
        finally:
            self.close()
