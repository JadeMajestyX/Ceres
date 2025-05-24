import customtkinter
import tkinter.messagebox as messagebox
from customtkinter import CTkComboBox
from config.security import check_password
from plant_manager import PlantManager
from models.plant_modal import PlantModal

# -- Paleta de colores --
BG = "#114c5f"
PANEL = "#9cd2d3"
ACCENT = "#0799b6"
ACCENT_DARK = "#4a6eb0"
FONT_LABEL = ("Arial", 20)
FONT_BUTTON = ("Arial", 18, "bold")

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
            self.selection_fr, values=self._get_plant_names(),
            command=self.on_select,
            border_color=ACCENT, button_color=ACCENT,
            dropdown_hover_color=ACCENT_DARK,
            font=("Arial", 18), state="readonly")
        self.combo.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")

        # Botones
        self._make_btn("+ Nueva Planta", self.add_modal, 2)
        self.btn_edit = self._make_btn("✏ Editar Planta", self.edit_modal, 3, False)
        self.btn_delete = self._make_btn("🗑 Eliminar Planta", self.delete_plant, 4, False)

        # Parámetros 
        self.params_fr = customtkinter.CTkScrollableFrame(
            self, label_text="Parámetros de la Planta",
            label_font=("Arial", 24, "bold"),
            label_text_color="white", fg_color=PANEL)
        self.params_fr.grid(row=2, column=0, rowspan=4,
                          padx=30, pady=(10, 25), sticky="nsew")
        self.params_fr.grid_columnconfigure(0, weight=1)

        # Guardar 
        self.btn_save = customtkinter.CTkButton(
            self, text="Guardar Cambios", state="disabled",
            font=("Arial", 20, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_DARK,
            command=self.save_params)
        self.btn_save.grid(row=6, column=0, pady=(0, 30), sticky="s")

        # Configuración de grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.current = None
        self.entry_refs = {}

    def _get_plant_names(self):
        plantas = self.manager.plants_model.obtener_todas_las_plantas()
        return [planta['nombre'] for planta in plantas]

    def _make_btn(self, text, cmd, col, enabled=True):
        btn = customtkinter.CTkButton(
            self.selection_fr, text=text, command=cmd,
            font=FONT_BUTTON, fg_color=BG, hover_color=ACCENT,
            state="normal" if enabled else "disabled")
        btn.grid(row=0, column=col, padx=5, pady=15)
        return btn

    def add_modal(self):
        PlantModal(
            self, mode="new",
            on_save=lambda n, d, p: self._add_plant(n, d, p))

    def edit_modal(self):
        if not self.current:
            return
            
        option_menu = customtkinter.CTkToplevel(self)
        option_menu.title("Opciones de Edición")
        option_menu.geometry("300x200")
        option_menu.after(0, option_menu.grab_set)
        
        customtkinter.CTkLabel(
            option_menu, text="¿Qué deseas editar?",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        def open_edit(mode):
            option_menu.destroy()
            PlantModal(
                self, mode="edit",
                initial_name=self.current,
                initial_desc=self.manager.get_desc(self.current),
                initial_params=self.manager.get_params(self.current),
                on_save=lambda n, d, p: self._edit_plant(n, d, p),
                edit_mode=mode)
        
        customtkinter.CTkButton(
            option_menu, text="Nombre y Descripción",
            command=lambda: open_edit("info")
        ).pack(pady=5, fill="x", padx=20)
        
        customtkinter.CTkButton(
            option_menu, text="Solo Parámetros",
            command=lambda: open_edit("params")
        ).pack(pady=5, fill="x", padx=20)
        
        customtkinter.CTkButton(
            option_menu, text="Todo (Nombre, Desc. y Paráms)",
            command=lambda: open_edit("all")
        ).pack(pady=5, fill="x", padx=20)

    def _add_plant(self, name, desc, params):
        try:
            if self.manager.add(name, desc, params):
                self._refresh_combo(select=name)
                messagebox.showinfo("Éxito", "Planta agregada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo agregar la planta")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la planta: {str(e)}")

    def _edit_plant(self, new_name, new_desc, new_params):
        try:
            # Si solo se editan parámetros (new_name y new_desc son None)
            if new_name is None and new_desc is None:
                if self.manager.save_params(self.current, new_params):
                    messagebox.showinfo("Éxito", "Parámetros actualizados correctamente")
                    self._refresh_combo(select=self.current)  # Mantener selección actual
            else:
                # Edición normal (nombre, desc y/o parámetros)
                if self.manager.update(self.current, new_name or self.current, 
                                     new_desc or self.manager.get_desc(self.current), 
                                     new_params):
                    self.current = new_name or self.current
                    self._refresh_combo(select=self.current)
                    messagebox.showinfo("Éxito", "Planta actualizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la planta: {str(e)}")

    def delete_plant(self):
        if not self.current:
            return

        if not messagebox.askyesno(
            "Eliminar planta",
            f"¿Seguro que quieres eliminar '{self.current}'?"
        ):
            return  

        if not check_password():
            return  

        try:
            plant_name = self.current
            self.manager.remove(plant_name)
            self._refresh_combo(select=None)
            self._clear_params()
            messagebox.showinfo("Éxito", f"La planta '{plant_name}' se eliminó correctamente")
            self.current = None
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la planta: {str(e)}")

    def _refresh_combo(self, select=None):
        self.combo.configure(values=self._get_plant_names())
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

        # Campos de parámetros
        params = self.manager.get_params(name)
        param_labels = [
            ("Temperatura mínima (°C)", "temp_min"),
            ("Temperatura máxima (°C)", "temp_max"),
            ("PH mínimo", "ph_min"),
            ("PH máximo", "ph_max"),
            ("EC mínimo (%)", "ec_min"),
            ("EC máximo (%)", "ec_max")
        ]

        self.entry_refs = {}
        for i, (label, key) in enumerate(param_labels, start=1):
            customtkinter.CTkLabel(
                self.params_fr, text=label, font=("Arial", 18),
                text_color="black"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            e = customtkinter.CTkEntry(
                self.params_fr, font=("Arial", 16),
                border_color=ACCENT, height=35)
            e.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            e.insert(0, params.get(key, ""))
            self.entry_refs[key] = e

    def save_params(self):
        if not self.current:
            return

        try:
            data = {k: e.get() for k, e in self.entry_refs.items()}
            if self.manager.save_params(self.current, data):
                messagebox.showinfo("Éxito", "Parámetros guardados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los parámetros: {str(e)}")

    def _clear_params(self):
        for widget in self.params_fr.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("1000x700")
    root.title("Demo — Gestión de Plantas")
    PlantsView(root).pack(fill="both", expand=True)
    root.mainloop()