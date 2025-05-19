import json
import tkinter.messagebox as messagebox
import customtkinter

def check_password() -> bool:
    #Pide contraseña y la compara con utils/config.json (clave 'password')
    prompt = customtkinter.CTkInputDialog(
        title="Confirmación",
        text="Para continuar, ingresa la contraseña:",
    )
    entered = (prompt.get_input() or "").strip()

    try:
        with open("utils/config.json", "r") as f:
            stored = json.load(f).get("password", "")
    except FileNotFoundError:
        messagebox.showerror("Error", "utils/config.json no encontrado.")
        return False

    if entered != stored:
        messagebox.showerror("Error", "Contraseña incorrecta.")
        return False
    return True
