from models.Model import Model
from decimal import Decimal

class parametrosModel(Model):
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

    #obtener parametros en array
    def obtener_parametros(self, planta_id):
        try:
            self.cursor.execute("SELECT * FROM parametros WHERE planta_id = %s", (planta_id,))
            resultados = self.cursor.fetchall()
            # Convertir Decimal a float
            resultados_convertidos = []
            for fila in resultados:
                fila_convertida = tuple(float(valor) if isinstance(valor, Decimal) else valor for valor in fila)
                resultados_convertidos.append(fila_convertida)
            return resultados_convertidos
        finally:
            self.close()

    def agregar_parametros(self, planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max):
        try:
            self.cursor.execute(
                "INSERT INTO parametros (planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max)
            )
            self.connection.commit()
        finally:
            self.close()

    def editar_parametros(self, id, planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max):
        try:
            self.cursor.execute(
                "UPDATE parametros SET planta_id = %s, temp_min = %s, temp_max = %s, ph_min = %s, ph_max = %s, ec_min = %s, ec_max = %s WHERE id = %s",
                (planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max, id)
            )
            self.connection.commit()
        finally:
            self.close()

    def obtener_parametro(self, planta_id, tipo):
        try:
            self.cursor.execute(
                "SELECT * FROM parametros WHERE planta_id = %s ORDER BY id DESC LIMIT 1",
                (planta_id,)
            )
            parametro = self.cursor.fetchone()
            if tipo == "tempmin":
                return parametro[2]
            elif tipo == "tempmax":
                return parametro[3]
            elif tipo == "phmin":
                return parametro[4]
            elif tipo == "phmax":
                return parametro[5]
            elif tipo == "ecmin":
                return parametro[6]
            elif tipo == "ecmax":
                return parametro[7]
        finally:
            self.close()