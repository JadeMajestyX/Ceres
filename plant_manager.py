from models.plantasModel import PlantasModel

class PlantManager:
    def __init__(self):
        self.plants_model = PlantasModel()
    
    def add(self, name: str, desc: str, params: dict):
        try:
            planta_id = self.plants_model.agregar_planta(name, desc)
            if planta_id:
                self.plants_model.guardar_parametros(planta_id, params)
            return True
        except Exception as e:
            print(f"Error al agregar planta: {e}")
            return False

    def remove(self, name: str):
        planta = self.plants_model.obtener_planta_por_nombre(name)
        self.plants_model.eliminar_planta_por_nombre(name)
        return planta['nombre'] if planta and 'nombre' in planta else None

    def update(self, old_name: str, new_name: str, new_desc: str, new_params: dict):
        try:
            # Actualizar planta
            if self.plants_model.actualizar_planta(old_name, new_name, new_desc):
                # Actualizar parámetros
                planta_id = self.plants_model.obtener_id_por_nombre(new_name)
                if planta_id:
                    self.plants_model.guardar_parametros(planta_id, new_params)
                return True
            return False
        except Exception as e:
            print(f"Error al actualizar planta: {e}")
            return False

    def get_desc(self, name: str) -> str:
        planta = self.plants_model.obtener_planta_por_nombre(name)
        return planta['descripcion'] if planta and planta['descripcion'] else ""

    def get_params(self, name: str) -> dict:
        planta = self.plants_model.obtener_planta_por_nombre(name)
        if not planta:
            return {}
        
        return {
            'temp_min': str(planta.get('temp_min', '')),
            'temp_max': str(planta.get('temp_max', '')),
            'ph_min': str(planta.get('ph_min', '')),
            'ph_max': str(planta.get('ph_max', '')),
            'ec_min': str(planta.get('ec_min', '')),
            'ec_max': str(planta.get('ec_max', ''))
        }