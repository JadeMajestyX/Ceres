from models.Model import Model

class MedicionesModel(Model):
    def __init__(self):
        super().__init__()

    def obtener_mediciones(self, planta_id):
        try:
            self.cursor.execute("SELECT * FROM mediciones WHERE planta_id = %s ORDER BY id DESC LIMIT 1", (planta_id,))
            return self.cursor.fetchone()
        finally:
            self.close()


    def agregar_medicion(self,planta_id ,temp_value: float ,ph_value: float ,ec_value: float, water_value: float):
        try:
            self.cursor.execute(
                "INSERT INTO mediciones (planta_id, temp_value, ph_value, ec_value, water_value) VALUES (%s,%s,%s,%s,%s)",
                (planta_id, temp_value, ph_value, ec_value, water_value)
            )
            self.connection.commit()
        finally:
            self.close()

    def obtener_medicion(self, planta_id, tipo):
        try:
            self.cursor.execute(
                "SELECT * FROM mediciones WHERE planta_id = %s ORDER BY id DESC LIMIT 1",
                (planta_id,)
            )
            medicion = self.cursor.fetchone()
            if tipo == "temp":
                return medicion[2]
            elif tipo == "ph":
                return medicion[3]
            elif tipo == "ec":
                return medicion[4]
            elif tipo == "water":
                return medicion[5]
            elif tipo == "time":
                return medicion[6]
            elif tipo == "id":
                return medicion[0]
            elif tipo == "planta_id":
                return medicion[1]
        finally:
            self.close()