from config.Database import Database
# from utils.functions.functions import update_planta

class PlantasModel:
    def __init__(self):
        self.db = Database()
    
    def agregar_planta(self, nombre: str, descripcion: str):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO plantas (nombre, descripcion) VALUES (%s, %s)",
                (nombre, descripcion)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar planta: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def eliminar_planta_por_nombre(self, nombre: str):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Primero obtener el ID para eliminar los parámetros
            planta_id = self.obtener_id_por_nombre(nombre)
            if planta_id:
                # Eliminar parámetros primero
                cursor.execute("DELETE FROM parametros WHERE planta_id = %s", (planta_id,))
                # Luego eliminar la planta
                cursor.execute("DELETE FROM plantas WHERE nombre = %s", (nombre,))
                conn.commit()
                return nombre
            else:
                return None
        except Exception as e:
            print(f"Error al eliminar planta: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def actualizar_planta(self, nombre_actual: str, nuevo_nombre: str, nueva_desc: str):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE plantas SET nombre = %s, descripcion = %s WHERE nombre = %s",
                (nuevo_nombre, nueva_desc, nombre_actual)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar planta: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def obtener_planta_por_nombre(self, nombre: str):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT p.*, par.temp_min, par.temp_max, par.ph_min, par.ph_max, 
                   par.ec_min, par.ec_max 
                   FROM plantas p 
                   LEFT JOIN parametros par ON p.id = par.planta_id 
                   WHERE p.nombre = %s""",
                (nombre,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener planta: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_planta_id(self, planta_id: int):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM plantas WHERE id = %s",
                (planta_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener planta por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()



    def obtener_todas_las_plantas(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT nombre FROM plantas ORDER BY nombre")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todas las plantas: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def obtener_id_por_nombre(self, nombre: str):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM plantas WHERE nombre = %s", (nombre,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error al obtener ID de planta: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def guardar_parametros(self, planta_id: int, parametros: dict):
        from utils.functions.functions import update_planta  # <--- importar dentro de la función
        update_planta(planta_id)
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Verificar si ya existen parámetros para esta planta
            cursor.execute("SELECT 1 FROM parametros WHERE planta_id = %s", (planta_id,))
            if cursor.fetchone():
                # Actualizar existente
                cursor.execute(
                    """UPDATE parametros SET 
                       temp_min = %s, temp_max = %s, 
                       ph_min = %s, ph_max = %s, 
                       ec_min = %s, ec_max = %s 
                       WHERE planta_id = %s""",
                    (parametros['temp_min'], parametros['temp_max'],
                     parametros['ph_min'], parametros['ph_max'],
                     parametros['ec_min'], parametros['ec_max'],
                     planta_id))
            else:
                # Insertar nuevo
                cursor.execute(
                    """INSERT INTO parametros 
                       (planta_id, temp_min, temp_max, ph_min, ph_max, ec_min, ec_max) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (planta_id, parametros['temp_min'], parametros['temp_max'],
                     parametros['ph_min'], parametros['ph_max'],
                     parametros['ec_min'], parametros['ec_max']))
            conn.commit()
        except Exception as e:
            print(f"Error al guardar parámetros: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()