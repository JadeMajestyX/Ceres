from models.plantasModel import PlantasModel

class PlantManager:
    def __init__(self):
        self.plants_model = PlantasModel()
    
    def add(self, name: str, desc: str):
        return self.plants_model.agregar_planta(name, desc)

    def remove(self, name: str):
        self.plants_model.eliminar_planta_por_nombre(name)

    def rename(self, old: str, new: str, desc: str):
        return self.plants_model.actualizar_planta(old, new, desc)

    def get_desc(self, name: str) -> str:
        planta = self.plants_model.obtener_planta_por_nombre(name)
        return planta['descripcion'] if planta and planta['descripcion'] else ""

    def save_params(self, name: str, params: dict):
        planta_id = self.plants_model.obtener_id_por_nombre(name)
        if planta_id:
            # Convertir los nombres de parámetros de la interfaz a los de la DB
            db_params = {
                'temp_min': params.get('Temperatura mínima (°C)', ''),
                'temp_max': params.get('Temperatura máxima (°C)', ''),
                'ph_min': params.get('PH mínimo', ''),
                'ph_max': params.get('PH máximo', ''),
                'ec_min': params.get('EC mínimo (%)', ''),
                'ec_max': params.get('EC máximo (%)', '')
            }
            self.plants_model.guardar_parametros(planta_id, db_params)

    def get_params(self, name: str) -> dict:
        planta = self.plants_model.obtener_planta_por_nombre(name)
        if not planta:
            return {}
        
        return {
            'Temperatura mínima (°C)': str(planta.get('temp_min', '')),
            'Temperatura máxima (°C)': str(planta.get('temp_max', '')),
            'PH mínimo': str(planta.get('ph_min', '')),
            'PH máximo': str(planta.get('ph_max', '')),
            'EC mínimo (%)': str(planta.get('ec_min', '')),
            'EC máximo (%)': str(planta.get('ec_max', ''))
        }