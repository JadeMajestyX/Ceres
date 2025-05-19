import customtkinter
import tkinter.messagebox as messagebox
from config.security import check_password

MAX_LEN = 20        # caracteres permitidos en nombre

class PlantModal(customtkinter.CTkToplevel):

    def __init__(self, master, mode="new",
                 initial_name="", initial_desc="",
                 on_save=lambda n, d: None):
        super().__init__(master)
        self.title("Nueva Planta" if mode == "new" else "Editar Planta")
        self.geometry("420x480")
        self.configure(fg_color="#f2e6cf")
        self.grab_set()
        self.on_save = on_save

        # -- Widgets --
        lbl_font = ("Arial", 20)
        self.name_lbl = customtkinter.CTkLabel(
            self, text="Nombre de la Planta:", font=lbl_font, text_color="#114c5f")
        self.name_lbl.pack(pady=(25, 5))

        vcmd = (self.register(self._limit_len), "%P")   # %P = nuevo valor
        self.name_entry = customtkinter.CTkEntry(
            self, font=("Arial", 22),
            border_color="#0799b6",
            validate="key", validatecommand=vcmd)
        self.name_entry.pack(pady=5, padx=30, fill="x")

        self.desc_lbl = customtkinter.CTkLabel(
            self, text="Descripción:", font=lbl_font, text_color="#114c5f")
        self.desc_lbl.pack(pady=(20, 5))

        self.desc_entry = customtkinter.CTkTextbox(
            self, font=("Arial", 20), height=160, border_color="#0799b6")
        self.desc_entry.pack(pady=5, padx=30, fill="both", expand=True)

        action = "Guardar" if mode == "new" else "Actualizar"
        self.save_btn = customtkinter.CTkButton(
            self, text=action, font=("Arial", 18, "bold"),
            fg_color="#114c5f", hover_color="#0799b6",
            command=self._confirm)
        self.save_btn.pack(pady=25)

        # Pre‑cargar valores si es edición
        self.name_entry.insert(0, initial_name)
        self.desc_entry.insert("0.0", initial_desc)

    # -- Validación de longitud ---
    def _limit_len(self, proposed: str) -> bool:
        """Valida en tiempo real que el nombre no exceda MAX_LEN."""
        return len(proposed) <= MAX_LEN

    # Botón Guardar / Actualizar 
    def _confirm(self):

        # borro avisos previos si existen
        for widget in getattr(self, "_warnings", []):
            widget.destroy()
        self._warnings = []

        name = self.name_entry.get().strip()
        desc = self.desc_entry.get("0.0", "end").strip()

          # Avisos
        if not name:
            warn = customtkinter.CTkLabel(
                self, text="*Los campos son obligatorios*",
                text_color="red", font=("Arial", 14))
            warn.pack(after=self.name_entry, pady=(0, 5))
            self._warnings.append(warn)

        if not desc:
            warn = customtkinter.CTkLabel(
                self, text="*Los campos son obligatorios*",
                text_color="red", font=("Arial", 14))
            warn.pack(after=self.desc_entry, pady=(0, 5))
            self._warnings.append(warn)

        # si falta algo, no continúo
        if not name or not desc:
            return
        # Longitud de nombre
        if len(name) > MAX_LEN:
            messagebox.showwarning(
                "Nombre muy largo",
                f"Máximo {MAX_LEN} caracteres. (Tienes {len(name)})")
            return

        if not check_password(): # Contraseña
            return

        self.on_save(name, desc)
        self.destroy()
