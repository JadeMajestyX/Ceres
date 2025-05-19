import customtkinter
import tkinter.messagebox as messagebox
from customtkinter import CTkComboBox
from config.security import check_password   #  NUEVO


from plant_manager import PlantManager
from models.plant_modal import PlantModal

# -- Paleta de colores de acuerdo a nuestro pi --
BG           = "#114c5f"
PANEL        = "#9cd2d3"
ACCENT       = "#0799b6"
ACCENT_DARK  = "#4a6eb0"
FONT_LABEL   = ("Arial", 20)
FONT_BUTTON  = ("Arial", 18, "bold")


class PlantsView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=BG)
        self.manager = PlantManager()

        # Título 
        title = customtkinter.CTkLabel(
            self, text="Gestión de Plantas",
            font=("Arial", 42, "bold"), text_color="white")
        title.grid(row=0, column=0, pady=(20, 30), sticky="n")

        # Frame selección
        self.selection_fr = customtkinter.CTkFrame(self, fg_color=PANEL)
        self.selection_fr.grid(row=1, column=0, padx=30, pady=15, sticky="ew")
        self.selection_fr.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(
            self.selection_fr, text="Seleccionar Planta:",
            font=FONT_LABEL, text_color=BG
        ).grid(row=0, column=0, padx=(15, 10), pady=15)

        self.combo = CTkComboBox(
            self.selection_fr, values=[],
            command=self.on_select,
            border_color=ACCENT, button_color=ACCENT,
            dropdown_hover_color=ACCENT_DARK,
            font=("Arial", 18), state="readonly")
        self.combo.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")

        # Botones
        self._make_btn("+ Nueva Planta", self.add_modal, 2)
        self.btn_edit   = self._make_btn("✏ Editar Planta", self.edit_modal, 3, False)
        self.btn_delete = self._make_btn("🗑 Eliminar Planta", self.delete_plant, 4, False)

        #  Parámetros 
        self.params_fr = customtkinter.CTkScrollableFrame(
            self, label_text="Parámetros de la Planta",
            label_font=("Arial", 24, "bold"),
            label_text_color="white", fg_color=PANEL)
        self.params_fr.grid(row=2, column=0, rowspan=4,
                            padx=30, pady=(10, 25), sticky="nsew")
        self.params_fr.grid_columnconfigure(0, weight=1)

        #  Guardar 
        self.btn_save = customtkinter.CTkButton(
            self, text="Guardar Cambios", state="disabled",
            font=("Arial", 20, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_DARK,
            command=self.save_params)
        self.btn_save.grid(row=6, column=0, pady=(0, 30), sticky="s")

        # Acomoda las filas/columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.current = None          # planta seleccionada
        self.entry_refs = {}         # param -> entry widget

    #Helper para botones 
    def _make_btn(self, text, cmd, col, enabled=True):
        btn = customtkinter.CTkButton(
            self.selection_fr, text=text, command=cmd,
            font=FONT_BUTTON, fg_color=BG, hover_color=ACCENT,
            state="normal" if enabled else "disabled")
        btn.grid(row=0, column=col, padx=5, pady=15)
        return btn

    # Modales 
    def add_modal(self):
        PlantModal(self, mode="new", on_save=self._add_plant)

    def edit_modal(self):
        if self.current:
            PlantModal(
                self, mode="edit",
                initial_name=self.current,
                initial_desc=self.manager.get_desc(self.current),
                on_save=lambda n, d: self._edit_plant(n, d, self.current))

    #  se hizo un CRUD interno 
    def _add_plant(self, name, desc):
        self.manager.add(name, desc)
        self._refresh_combo(select=name)

    def _edit_plant(self, new_name, new_desc, old_name):
        if new_name != old_name:
            self.manager.rename(old_name, new_name)
        self.manager.add(new_name, new_desc)       # actualiza desc.
        self._refresh_combo(select=new_name)


    def delete_plant(self):
        if not self.current:
            return

        # guardamos el nombre actual antes de eliminar
        plant_name = self.current

        # la confirmación de usuario
        if not messagebox.askyesno(
            "Eliminar planta",
            f"¿Seguro que quieres eliminar '{plant_name}'?"
        ):
            return  

        # solicita contraseña
        if not check_password():          #security.check_password()
            return  

        self.manager.remove(plant_name)
        self._refresh_combo(select=None)
        self._clear_params()
        messagebox.showinfo(
            "Eliminado",
            f"La planta '{plant_name}' se eliminó correctamente."
        )


    # ComboBox
    def _refresh_combo(self, select=None):
        self.combo.configure(values=list(self.manager.descriptions.keys()))
        self.combo.set(select or "")
        self.on_select(select)

    def on_select(self, name):
        self.current = name
        self.btn_edit.configure(state="normal" if name else "disabled")
        self.btn_delete.configure(state="normal" if name else "disabled")
        self.btn_save.configure(state="normal" if name else "disabled")
        self._clear_params()
        if not name:
            return

        # Descripción
        desc = self.manager.get_desc(name)
        customtkinter.CTkLabel(
            self.params_fr, text=f"Descripción: {desc}",
            wraplength=500, font=("Arial", 18), text_color="black"
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Campos
        params = [
            "EC mínimo (%)", "EC máximo (%)",
            "Temperatura mínima (°C)", "Temperatura máxima (°C)",
            "PH mínimo", "PH máximo",
        ]
        self.entry_refs = {}
        for i, p in enumerate(params, start=1):
            customtkinter.CTkLabel(
                self.params_fr, text=p, font=("Arial", 18),
                text_color="black"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="w")
            e = customtkinter.CTkEntry(
                self.params_fr, font=("Arial", 16),
                border_color=ACCENT, height=35)
            e.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            # precargar si existían
            e.insert(0, self.manager.get_params(name).get(p, ""))
            self.entry_refs[p] = e

    #  Guardar parámetros 
    def save_params(self):
        if not self.current:
            return
        data = {k: e.get() for k, e in self.entry_refs.items()}
        self.manager.save_params(self.current, data)
        messagebox.showinfo("Guardado", "Parámetros guardados correctamente.")

    def _clear_params(self):
        for w in self.params_fr.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("1000x700")
    root.title("Demo — Gestión de Plantas")
    PlantsView(root).pack(fill="both", expand=True)
    root.mainloop()
