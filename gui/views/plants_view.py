import customtkinter
import os
import json
from customtkinter import CTkComboBox
import tkinter.messagebox as messagebox

class PlantsView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color="#114c5f")  # Fondo: Sinbad
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        self.title_label = customtkinter.CTkLabel(
            self, text="Gestión de Plantas", 
            font=("Arial", 42, "bold"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, pady=(20, 30), sticky="n")
        
        
        self.selection_frame = customtkinter.CTkFrame(self, fg_color="#9cd2d3")
        self.selection_frame.grid(row=1, column=0, padx=30, pady=15, sticky="ew")
        
        self.plant_selector_label = customtkinter.CTkLabel(
            self.selection_frame, 
            text="Seleccionar Planta:",
            font=("Arial", 20),
            text_color="#114c5f"
        )
        self.plant_selector_label.pack(side="left", padx=(15, 10), pady=15)
        
        self.plant_selector = CTkComboBox(
            self.selection_frame, 
            values=["Lechuga"],
            command=self.on_plant_selected,
            border_color="#0799b6",
            button_color="#0799b6",
            dropdown_hover_color="#4a6eb0",
            font=("Arial", 18),
            state="readonly"
        )
        self.plant_selector.set("")
        self.plant_selector.pack(side="left", padx=(0, 15), pady=15, fill="x", expand=True)
        
        self.add_plant_btn = customtkinter.CTkButton(
            self.selection_frame, 
            text="+ Nueva Planta", 
            command=self.add_new_plant,
            font=("Arial", 18, "bold"),
            fg_color="#114c5f",
            hover_color="#0799b6"
        )
        self.add_plant_btn.pack(side="right", padx=(10, 25), pady=15)
        
        self.parameters_frame = customtkinter.CTkScrollableFrame(
            self, label_text="Parámetros de la Planta",
            label_text_color="white",
            fg_color="#9cd2d3",
            label_font=("Arial", 24, "bold")
        )
        self.parameters_frame.grid(row=2, column=0, rowspan=4, padx=30, pady=(10, 25), sticky="nsew")
        self.parameters_frame.grid_columnconfigure(0, weight=1)
        
        self.param_entries = {}
        
        self.save_btn = customtkinter.CTkButton(
            self, 
            text="Guardar Cambios", 
            command=self.save_parameters, 
            state="disabled",
            font=("Arial", 20, "bold"),
            fg_color="#0799b6",
            hover_color="#4a6eb0"
        )
        self.save_btn.grid(row=6, column=0, pady=(0, 30), sticky="s")
        
        self.current_plant = None
        self.plant_descriptions = {}

    def add_new_plant(self):
        self.new_plant_window = customtkinter.CTkToplevel(self)
        self.new_plant_window.title("Nueva Planta")
        self.new_plant_window.geometry("400x450")
        self.new_plant_window.configure(fg_color="#f2e6cf")
        
        self.new_plant_window.update_idletasks()
        self.new_plant_window.deiconify()
        self.new_plant_window.grab_set()
        
        x = (self.new_plant_window.winfo_screenwidth() // 2) - 200
        y = (self.new_plant_window.winfo_screenheight() // 2) - 225
        self.new_plant_window.geometry(f"400x450+{x}+{y}")
        
        self.name_label = customtkinter.CTkLabel(
            self.new_plant_window, 
            text="Nombre de la Planta:", 
            font=("Arial", 18),
            text_color="#114c5f"
        )
        self.name_label.pack(pady=(20, 5))
        
        self.name_entry = customtkinter.CTkEntry(
            self.new_plant_window, 
            font=("Arial", 20), 
            border_color="#0799b6", 
            height=35
        )
        self.name_entry.pack(pady=5, padx=30, fill="x")
        
        self.desc_label = customtkinter.CTkLabel(
            self.new_plant_window, 
            text="Descripción:", 
            font=("Arial", 18),
            text_color="#114c5f",
        )
        self.desc_label.pack(pady=(20, 5))
        
        self.desc_entry = customtkinter.CTkTextbox(
            self.new_plant_window, 
            width=320,
            height=150, 
            font=("Arial", 20),
            border_color="#0799b6", 
        )
        self.desc_entry.pack(pady=5, padx=30, fill="x", expand=True)
        
        self.confirm_button = customtkinter.CTkButton(
            self.new_plant_window, 
            text="Guardar", 
            font=("Arial", 18, "bold"),
            command=self.save_new_plant,
            fg_color="#114c5f",
            hover_color="#0799b6"
        )
        self.confirm_button.pack(pady=20)

    def save_new_plant(self):
            plant_name = self.name_entry.get().strip()
            plant_desc = self.desc_entry.get("0.0","end").strip()

            # Validación nombre
            if not plant_name:
                if not hasattr(self, "name_error_label") or not self.name_error_label.winfo_exists():
                    self.name_error_label = customtkinter.CTkLabel(
                        self.new_plant_window,
                        text="*Este campo es obligatorio*",
                        text_color="red",
                        font=("Arial", 14)
                    )
                    self.name_error_label.pack(after=self.name_entry, pady=(0, 5))
            else:
                if hasattr(self, "name_error_label") and self.name_error_label.winfo_exists():
                    self.name_error_label.destroy()

            # Validación descripción
            if not plant_desc:
                if not hasattr(self, "desc_error_label") or not self.desc_error_label.winfo_exists():
                    self.desc_error_label = customtkinter.CTkLabel(
                        self.new_plant_window,
                        text="*Este campo es obligatorio*",
                        text_color="red",
                        font=("Arial", 14)
                    )
                    self.desc_error_label.pack(after=self.desc_entry, pady=(0, 5))
            else:
                if hasattr(self, "desc_error_label") and self.desc_error_label.winfo_exists():
                    self.desc_error_label.destroy()

            if not plant_name or not plant_desc:
                return

            # Preguntar contraseña
            password_prompt = customtkinter.CTkInputDialog(
                title="Confirmación",
                text="Para guardar, ingresa la contraseña:"
            )
            input_password = password_prompt.get_input().strip()

            try:
                with open("utils/config.json", "r") as f:
                    config = json.load(f)
                    stored_password = config.get("password", "")
            except FileNotFoundError:
                messagebox.showerror("Error", "Archivo de configuración no encontrado.")
                return
            print(f"Contraseña ingresada: '{input_password}'")
            print(f"Contraseña esperada: '{stored_password}'")

            if input_password != stored_password:
                messagebox.showerror("Contraseña incorrecta", "La contraseña ingresada no es correcta.")
                return

            # Guardar planta
            if plant_name not in self.plant_selector.cget("values"):
                plant_options = list(self.plant_selector.cget("values"))
                plant_options.append(plant_name)
                self.plant_selector.configure(values=plant_options)

                self.plant_descriptions[plant_name] = plant_desc
                self.new_plant_window.destroy()
                self.plant_selector.set(plant_name)
                self.on_plant_selected(plant_name)
                messagebox.showinfo("Éxito", f"Planta '{plant_name}' guardada correctamente.")
            else:
                messagebox.showwarning("Duplicado", "La planta ya existe.")

                    


    def on_plant_selected(self, selected_plant):
        self.current_plant = selected_plant
        self.clear_parameters_frame()
        
        if selected_plant:
            self.param_entries = {}
            
            desc_text = self.plant_descriptions.get(selected_plant, "La lechugas son plantas anuales o bienales, autógamas, de porte erecto y hasta 1 m de altura, lampiñas y con tallos ramificados."
                                                                    "Caracteristicas: 9 pares de costillas, pico de 6-8 mm, no alados y con vilano de 2 filas de pelos blancos y simples. 2n = 18, 36."
                                                                    "Se cultiva por sus hojas que se comen en ensalada y como verdura."
                                                                    "Multiplica por semilla")
            desc_label = customtkinter.CTkLabel(
                self.parameters_frame, 
                text=f"Descripción: {desc_text}",
                wraplength=500,
                font=("Arial", 18),
                text_color="black"
            )
            desc_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")


            parameters = [
                "EC mínimo (%)",
                "EC máximo (%)",
                "Temperatura mínima (°C)",
                "Temperatura máxima (°C)",
                "PH mínimo",
                "PH máximo"
            ]

            for i, param in enumerate(parameters):
                label = customtkinter.CTkLabel(
                    self.parameters_frame, 
                    text=param, 
                    font=("Arial", 18),
                    text_color="black"
                )
                label.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
                entry = customtkinter.CTkEntry(
                    self.parameters_frame, 
                    font=("Arial", 16), 
                    border_color="#0799b6", 
                    height=35
                )
                entry.grid(row=i+1, column=1, padx=10, pady=10, sticky="ew")
                self.param_entries[param] = entry

            self.save_btn.configure(state="normal")
        else:
            self.save_btn.configure(state="disabled")

    def clear_parameters_frame(self):
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()

    def save_parameters(self):
        if self.current_plant:
            params = {param: entry.get() for param, entry in self.param_entries.items()}
            print(f"Parámetros guardados para {self.current_plant}: {params}")

