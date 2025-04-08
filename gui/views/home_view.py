# home_view.py
import customtkinter

class HomeView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.button = customtkinter.CTkButton(self, text="Hola")
        self.button.pack(padx=20, pady=20)
