from models.Model import Model

class AlertasModel(Model):
    def __init__(self):
        super().__init__()

    def obtener_alertas(self, planta_id, resulta: bool = False):
        try:
            self.cursor.execute("SELECT * FROM alertas WHERE planta_id = %s AND resuelta = %s ORDER BY id DESC", (planta_id, resulta))
            return self.cursor.fetchall()
        finally:
            self.close()

    def obtener_todas_alertas(self, planta_id):
        try:
            # Obtener todas las alertas para la planta_id
            self.cursor.execute(
                "SELECT * FROM alertas WHERE planta_id = %s ORDER BY id DESC", 
                (planta_id,)
            )
            return self.cursor.fetchall()  # Devuelve todas las alertas para la planta_id
        finally:
            self.close()

    def agregar_alerta(self, planta_id, mensaje, medicion_id=None):
        try:
            # 1. Verificar si ya existe una alerta igual sin resolver
            self.cursor.execute(
                "SELECT id FROM alertas WHERE planta_id = %s AND mensaje = %s AND resuelta = FALSE ORDER BY id DESC LIMIT 1",
                (planta_id, mensaje)
            )
            alerta_existente = self.cursor.fetchone()

            if alerta_existente:
                # Ya existe una alerta igual sin resolver, no insertamos
                return
            
            # 2. Si no existe, insertar nueva alerta
            self.cursor.execute(
                "INSERT INTO alertas (planta_id, medicion_id, mensaje) VALUES (%s, %s, %s)",
                (planta_id, medicion_id, mensaje)
            )
            self.connection.commit()
        finally:
            self.close()

    def alerta_solucionada(self, planta_id, mensaje):
        try:
            # Actualizar la alerta, marcándola como solucionada (resuelta = True)
            self.cursor.execute(
                "UPDATE alertas SET resuelta = %s WHERE planta_id = %s AND resuelta = %s AND mensaje = %s ",
                (True, planta_id, False, mensaje)  # Se actualiza solo las alertas no resueltas
            )
            self.connection.commit()  # Asegurarse de guardar los cambios
        finally:
            self.close()
