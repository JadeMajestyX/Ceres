import customtkinter
import tkinter.messagebox as messagebox
from config.security import check_password

MAX_LEN = 20  # caracteres permitidos en nombre

class PlantModal(customtkinter.CTkToplevel):
    def __init__(self, master, mode="new",
                 initial_name="", initial_desc="",
                 initial_params=None,
                 on_save=None, edit_mode="all"):
        super().__init__(master)
        self.title("Nueva Planta" if mode == "new" else "Editar Planta")
        self.geometry("500x700")
        self.configure(fg_color="#f2e6cf")
        self.grab_set()
        if on_save is None:
            def on_save(name, desc, params):
                pass
        self.on_save = on_save
        self.entry_refs = {}
        self.edit_mode = edit_mode  # "all", "info", "params"

        # -- Widgets principales --
        lbl_font = ("Arial", 20)
        
        if self.edit_mode in ["all", "info"]:
            self.name_lbl = customtkinter.CTkLabel(
                self, text="Nombre de la Planta:", font=lbl_font, text_color="#114c5f")
            self.name_lbl.pack(pady=(15, 5))

            vcmd = (self.register(self._limit_len), "%P")
            self.name_entry = customtkinter.CTkEntry(
                self, font=("Arial", 22),
                border_color="#0799b6",
                validate="key", validatecommand=vcmd)
            self.name_entry.pack(pady=5, padx=30, fill="x")

            self.desc_lbl = customtkinter.CTkLabel(
                self, text="Descripción:", font=lbl_font, text_color="#114c5f")
            self.desc_lbl.pack(pady=(15, 5))

            self.desc_entry = customtkinter.CTkTextbox(
                self, font=("Arial", 20), height=120, border_color="#0799b6")
            self.desc_entry.pack(pady=5, padx=30, fill="x")
        else:
            # Mostrar nombre como label si solo se editan parámetros
            self.name_lbl = customtkinter.CTkLabel(
                self, text=f"Planta: {initial_name}", font=lbl_font, text_color="#114c5f")
            self.name_lbl.pack(pady=(15, 5))

        # -- Frame de parámetros --
        self.params_frame = customtkinter.CTkFrame(self, fg_color="#e6d9bf")
        self.params_frame.pack(pady=(15, 5), padx=30, fill="both", expand=True)

        param_labels = [
            ("Temperatura mínima (°C)", "temp_min"),
            ("Temperatura máxima (°C)", "temp_max"),
            ("PH mínimo", "ph_min"),
            ("PH máximo", "ph_max"),
            ("EC mínimo (%)", "ec_min"),
            ("EC máximo (%)", "ec_max")
        ]

        for i, (label, key) in enumerate(param_labels):
            customtkinter.CTkLabel(
                self.params_frame, text=label, font=("Arial", 16),
                text_color="#114c5f"
            ).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            entry = customtkinter.CTkEntry(
                self.params_frame, font=("Arial", 16),
                border_color="#0799b6", width=150)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="e")
            self.entry_refs[key] = entry

        # -- Botón de acción --
        action = "Guardar" if mode == "new" else "Actualizar"
        self.save_btn = customtkinter.CTkButton(
            self, text=action, font=("Arial", 18, "bold"),
            fg_color="#114c5f", hover_color="#0799b6",
            command=self._confirm)
        self.save_btn.pack(pady=15)

        # Pre-cargar valores si es edición
        if self.edit_mode in ["all", "info"]:
            self.name_entry.insert(0, initial_name)
            self.desc_entry.insert("0.0", initial_desc)
        
        if initial_params:
            for key, entry in self.entry_refs.items():
                entry.insert(0, initial_params.get(key, ""))

    def _limit_len(self, proposed: str) -> bool:
        return len(proposed) <= MAX_LEN

    def _confirm(self):
        # Validación de campos obligatorios
        name = self.name_entry.get().strip() if self.edit_mode in ["all", "info"] else None
        desc = self.desc_entry.get("0.0", "end").strip() if self.edit_mode in ["all", "info"] else None
        
        if self.edit_mode in ["all", "info"] and (not name or not desc):
            messagebox.showwarning("Campos obligatorios", 
                                 "Nombre y descripción son campos obligatorios")
            return

        if name and len(name) > MAX_LEN:
            messagebox.showwarning(
                "Nombre muy largo",
                f"Máximo {MAX_LEN} caracteres. (Tienes {len(name)})")
            return

        if not check_password():
            return

        # Obtener parámetros
        params = {key: entry.get() for key, entry in self.entry_refs.items()}
        
        # Llamar al callback con todos los datos
        self.on_save(name, desc, params)
        self.destroy()