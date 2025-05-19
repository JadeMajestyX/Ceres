
class PlantManager:
    def __init__(self):
        self.descriptions: dict[str, str] = {}   # nombre → descripción
        self.parameters: dict[str, dict] = {}    # nombre → {param: valor}

    # ---- Descripciones ----
    def add(self, name: str, desc: str):
        self.descriptions[name] = desc

    def remove(self, name: str):
        self.descriptions.pop(name, None)
        self.parameters.pop(name, None)

    def rename(self, old: str, new: str):
        self.descriptions[new] = self.descriptions.pop(old)
        if old in self.parameters:
            self.parameters[new] = self.parameters.pop(old)

    def get_desc(self, name: str) -> str:
        return self.descriptions.get(name, "")

    # ---- Parámetros ----
    def save_params(self, name: str, params: dict[str, str]):
        self.parameters[name] = params

    def get_params(self, name: str) -> dict[str, str]:
        return self.parameters.get(name, {})
