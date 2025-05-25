import customtkinter

class ConfigView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        label = customtkinter.CTkLabel(self, text="Vista de Configuración", font=("Arial", 20))
        label.pack(pady=20)
