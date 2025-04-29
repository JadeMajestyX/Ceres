import customtkinter
from PIL import Image
import os

class ActuatorsView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#114C5F")
        # Directorio de iconos
        base = os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.abspath(os.path.join(base, '..', '..', 'assets', 'images'))
        # Configuración grid principal
        self.configure_grid()
        # Crear filas de actuadores
        self.create_actuator_containers()

    def configure_grid(self):
        """Configura filas y columna única con altura mínima"""
        for i in range(4):
            self.grid_rowconfigure(i, weight=1, minsize=220)
        self.grid_columnconfigure(0, weight=1)

    def create_actuator_containers(self):
        """Define datos y crea cada recuadro"""
        actuators = [
            ("Conductividad Eléctrica", "CE.png", "Los actuadores activan bombas dosificadoras para ajustar la concentración de nutrientes cuando la CE está fuera del rango ideal."),
            ("pH", "ph.png", "Se usan bombas para añadir soluciones ácidas o básicas y mantener el pH dentro del nivel óptimo para las plantas."),
            ("Temperatura", "Temp.png", "Ventiladores o calentadores se activan automáticamente para regular la temperatura del agua o ambiente."),
            ("Nivel de Agua", "LW.png", "Una bomba se activa cuando el nivel de agua baja, asegurando que siempre haya suficiente líquido para las raíces."),
        ]
        for idx, (title, ico, desc) in enumerate(actuators):
            icon_path = os.path.join(self.icon_dir, ico)
            self.create_actuator_box(idx, title, icon_path, desc)

    def create_actuator_box(self, row, title, icon_path, description):
        """Crea una fila con columnas de ancho fijo y contenido centrado"""
        box = customtkinter.CTkFrame(self, fg_color="#0089A3", corner_radius=12)
        box.grid(row=row, column=0, padx=20, pady=20, sticky="nsew")
                # Definir ancho mínimo de columnas y permitir expansión equitativa
        col_widths = [300, 120, 500, 220, 100]
        for i, width in enumerate(col_widths):
            box.grid_columnconfigure(i, weight=1, minsize=width, uniform="col")
        box.grid_rowconfigure(0, weight=1)

        # Título centrado
        lbl_title = customtkinter.CTkLabel(
            box,
            text=title,
            font=("Arial", 24, "bold"),
            text_color="white",
            wraplength=col_widths[0] - 20,
            justify="center"
        )
        lbl_title.grid(row=0, column=0, sticky="ns", padx=10)

        # Icono centrado
        try:
            img = customtkinter.CTkImage(
                light_image=Image.open(icon_path), size=(80, 80)
            )
        except Exception as e:
            print(f"Error cargando icono {icon_path}: {e}")
            img = None
        lbl_icon = customtkinter.CTkLabel(box, image=img, text="", fg_color="#0089A3")
        lbl_icon.grid(row=0, column=1, sticky="ns", padx=10)

        # Descripción en recuadro blanco, centrada
        desc_frame = customtkinter.CTkFrame(box, fg_color="white", corner_radius=10)
        desc_frame.grid(row=0, column=2, sticky="ns", padx=(10, 20))  # margen extra a la derecha
        desc_frame.grid_rowconfigure(0, weight=1)
        desc_frame.grid_columnconfigure(0, weight=1)
        lbl_desc = customtkinter.CTkLabel(
            desc_frame,
            text=description,
            font=("Arial", 16),
            text_color="black",
            wraplength=col_widths[2] - 40,  # menor wrap para margen interno
            justify="center"
        )
        lbl_desc.grid(row=0, column=0, sticky="nsew", padx=10, pady=1)

        # Switch ON/OFF grande y centrado
                # Switch ON/OFF grande y centrado
        switch = customtkinter.CTkSwitch(
        box,
        text="",
        fg_color="#FF8F8F",
        progress_color="#B6E880",
        button_color="white",
        width=120,
        height=60,
        font=("Arial", 24),  # Aumenta el tamaño visual del texto (aunque lo ocultamos)
        )


        switch.grid(row=0, column=3, sticky="ns", padx=10)

        # Botón ajustes centrado
        gear_path = os.path.join(self.icon_dir, "settings.png")
        try:
            gear_img = customtkinter.CTkImage(
                light_image=Image.open(gear_path), size=(80, 80)
            )
        except Exception as e:
            print(f"Error cargando engrane {gear_path}: {e}")
            gear_img = None
        btn = customtkinter.CTkButton(
            box,
            image=gear_img,
            text="",
            fg_color="transparent",
            hover_color="gray20",
            width=80,
            height=80,
            command=lambda t=title: self.open_settings(t)
        )
        btn.grid(row=0, column=4, sticky="ns", padx=10)

    def open_settings(self, title):
        """Abre modal de configuración para el actuador"""
        win = customtkinter.CTkToplevel(self)
        win.title(f"Configuración - {title}")
        win.geometry("600x400")

class ConfigOptions(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, fg_color="#114C5F", *args, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        lbl = customtkinter.CTkLabel(
            self,
            text="Configuración de Actuador",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        lbl.pack(pady=20)
        frame_i = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_i.pack(padx=20, pady=20, fill="x")
        customtkinter.CTkLabel(frame_i, text="Intervalo:", text_color="white").pack(side="left")
        self.interval = customtkinter.CTkOptionMenu(
            frame_i,
            values=["10 minutos", "30 minutos", "Siempre"],
            fg_color="#408DA6",
            button_color="#408DA6",
            dropdown_fg_color="#0089A3",
            width=150
        )
        self.interval.pack(side="right")
        frame_d = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_d.pack(padx=20, pady=20, fill="x")
        customtkinter.CTkLabel(frame_d, text="Días:", text_color="white").pack(side="left")
        for d in ["L","M","X","J","V","S","D"]:
            chk = customtkinter.CTkCheckBox(frame_d, text=d, fg_color="transparent")
            chk.pack(side="left", padx=10)
        btn_save = customtkinter.CTkButton(
            self,
            text="Guardar",
            fg_color="#F18F01",
            hover_color="#D17E00",
            width=180,
            height=60
        )
        btn_save.pack(pady=30)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    root = customtkinter.CTk()
    root.geometry("1200x900")
    root.title("Vista de Actuadores")
    ActuatorsView(root).pack(fill="both", expand=True)
    root.mainloop()
