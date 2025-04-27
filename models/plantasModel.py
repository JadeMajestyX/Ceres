from Model import Model

class PlantasModel(Model):
    def __init__(self):
        super().__init__()

    def obtener_plantas(self):
        try:
            self.cursor.execute("SELECT * FROM plantas")
            return self.cursor.fetchall()
        finally:
            self.close()

    def agregar_planta(self, nombre, descripcion):
        try:
            self.cursor.execute(
                "INSERT INTO plantas (nombre, descripcion) VALUES (%s, %s)",
                (nombre, descripcion)
            )
            self.connection.commit()
        finally:
            self.close()

    def obtener_planta(self, id):
        try:
            self.cursor.execute("SELECT * FROM plantas WHERE id = %s", (id,))
            return self.cursor.fetchone()
        finally:
            self.close()
