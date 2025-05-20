import customtkinter
from PIL import Image
import os

class ActuatorsView(customtkinter.CTkFrame):
    """
    Vista de Actuadores en una sola columna, similar a SensoresView.
    """
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
        """Configura filas y columna única con altura adaptable"""
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_actuator_containers(self):
        """Define datos y crea cada recuadro"""
        actuators = [
            ("Conductividad Eléctrica", "CE.png", 
             "Los actuadores activan bombas dosificadoras para ajustar la concentración de nutrientes cuando la CE está fuera del rango ideal.", "#A6F0FF"),
            ("pH", "ph.png", 
             "Se usan bombas para añadir soluciones ácidas o básicas y mantener el pH dentro del nivel óptimo para las plantas.", "#B2CDFF"),
            ("Temperatura", "Temp.png", 
             "Ventiladores o calentadores se activan automáticamente para regular la temperatura del agua o ambiente.", "#87E2FF"),
            ("Nivel de Agua", "LW.png", 
             "Una bomba se activa cuando el nivel de agua baja, asegurando que siempre haya suficiente líquido para las raíces.", "#FFF8E9"),
        ]
        for idx, (title, ico, desc, icon_color) in enumerate(actuators):
            icon_path = os.path.join(self.icon_dir, ico)
            self.create_actuator_box(idx, title, icon_path, desc, icon_color)

    def create_actuator_box(self, row, title, icon_path, description, icon_color):
        """Crea una fila con columnas de ancho adaptable y contenido centrado"""
        # Frame principal 
        box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=12)
        box.grid(row=row, column=0, padx=20, pady=20, sticky="nsew")

        # Configuración del grid
        col_weights = [2, 1, 3, 2, 1]
        for i, weight in enumerate(col_weights):
            box.grid_columnconfigure(i, weight=weight, uniform="col")
        box.grid_rowconfigure(0, weight=1)
        # Título centrado
        lbl_title = customtkinter.CTkLabel(
            box,
            text=title,
            font=("Arial", 24, "bold"),
            text_color="#393939",
            wraplength=300,
            justify="center"
        )
        lbl_title.grid(row=0, column=0, sticky="nsew", padx=10)

        # Icono centrado
        try:
            img = customtkinter.CTkImage(
                light_image=Image.open(icon_path), size=(80, 80)
            )
        except Exception as e:
            print(f"Error cargando icono {icon_path}: {e}")
            img = None
        lbl_icon = customtkinter.CTkLabel(box, image=img, text="", fg_color=icon_color)
        lbl_icon.grid(row=0, column=1, sticky="nsew", padx=10)

        # Descripción en recuadro blanco
        desc_frame = customtkinter.CTkFrame(box, fg_color="#FFFFFF", corner_radius=15)
        desc_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 10), pady=20)
        desc_frame.grid_rowconfigure(0, weight=1)
        desc_frame.grid_columnconfigure(0, weight=1)
        lbl_desc = customtkinter.CTkLabel(
            desc_frame,
            text=description,
            font=("Arial", 16),
            text_color="#393939",
            wraplength=400,
            justify="center"
        )
        lbl_desc.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Botón toggle personalizado con imágenes
        toggle_on_path = os.path.join(self.icon_dir, "ToggleON.png")
        toggle_off_path = os.path.join(self.icon_dir, "ToggleOFF.png")
        try:
            on_img_pil = Image.open(toggle_on_path).convert("RGBA")
            off_img_pil = Image.open(toggle_off_path).convert("RGBA")
            on_img = customtkinter.CTkImage(light_image=on_img_pil, size=(100, 60))
            off_img = customtkinter.CTkImage(light_image=off_img_pil, size=(100, 60))
        except Exception as e:
            print(f"Error cargando iconos toggle: {e}")
            on_img = off_img = None
        switch_btn = customtkinter.CTkButton(
            box,
            image=off_img,
            text="",
            fg_color="#9CD2D3",
            hover_color="#9CD2D3",
            width=100,
            height=60
        )
        switch_btn.grid(row=0, column=3, padx=10, pady=0)
        switch_btn.is_on = False
        def toggle_state(btn=switch_btn, img_on=on_img, img_off=off_img):
            btn.is_on = not btn.is_on
            btn.configure(image= img_on if btn.is_on else img_off)
        switch_btn.configure(command=toggle_state)

        # Botón ajustes con fondo del recuadro
        gear_path = os.path.join(self.icon_dir, "settings.png")
        try:
            pil_img = Image.open(gear_path).convert("RGBA")
            datas = pil_img.getdata()
            newData = []
            for item in datas:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            pil_img.putdata(newData)
            gear_img = customtkinter.CTkImage(light_image=pil_img, size=(80, 80))
        except Exception as e:
            print(f"Error cargando engrane {gear_path}: {e}")
            gear_img = None
        btn = customtkinter.CTkButton(
            box,
            image=gear_img,
            text="",
            fg_color="#9CD2D3",
            hover_color="#9CD2D3",
            width=80,
            height=80,
            command=lambda t=title: self.open_settings(t)
        )
        btn.grid(row=0, column=4, sticky="nsew", padx=10)

    def open_settings(self, title):
        """Abre modal de configuración para el actuador"""
        win = customtkinter.CTkToplevel(self)
        win.title(f"Configuración - {title}")
        win.geometry("600x270")

        win.lift()
        win.grab_set()
        win.focus_force()

        ConfigOptions(win).pack(fill="both", expand=True)


class ConfigOptions(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, fg_color="#114C5F", *args, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.abspath(os.path.join(base, '..', '..', 'assets', 'images'))

        lbl = customtkinter.CTkLabel(
            self,
            text="Configuración de Actuador",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        lbl.pack(pady=20)

        frame_i = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_i.pack(padx=20, pady=(20, 10), fill="x")
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

        frame_c = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_c.pack(padx=20, pady=(0, 20), fill="x")
        frame_c.grid_columnconfigure(1, weight=1)

        lbl_cal = customtkinter.CTkLabel(frame_c, text="Calibración:", text_color="white")
        lbl_cal.grid(row=0, column=0, padx=(0,10), pady=5)

        self.calibration_slider = customtkinter.CTkSlider(
            frame_c,
            from_=0.1,
            to=1.0,
            number_of_steps=9,
            command=self.update_calibration_value
        )
        self.calibration_slider.set(0.5)
        self.calibration_slider.grid(row=0, column=1, sticky="ew", pady=5)

        self.calibration_value_label = customtkinter.CTkLabel(
            frame_c,
            text=f"{self.calibration_slider.get():.2f}",
            text_color="white"
        )
        self.calibration_value_label.grid(row=0, column=2, padx=(10,0))

        save_path = os.path.join(self.icon_dir, "SaveIcon.png")
        try:
            pil_save = Image.open(save_path).convert("RGBA")
            save_img = customtkinter.CTkImage(light_image=pil_save, size=(24,24))
        except Exception as e:
            print(f"Error cargando icono de guardar {save_path}: {e}")
            save_img = None

        btn_save = customtkinter.CTkButton(
            self,
            text="Guardar",
            image=save_img,
            compound="left",
            fg_color="#F18F01",
            hover_color="#D17E00",
            width=180,
            height=40,
            command=self.save_settings
        )
        btn_save.pack(pady=20)

    def update_calibration_value(self, value):
        self.calibration_value_label.configure(text=f"{float(value):.2f}")

    def save_settings(self):
        intervalo = self.interval.get()
        calibracion = self.calibration_slider.get()
        print(f"Guardando - Intervalo: {intervalo}, Calibración: {calibracion}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    root = customtkinter.CTk()
    root.geometry("1200x900")
    root.title("Vista de Actuadores")
    ActuatorsView(root).pack(fill="both", expand=True)
    root.mainloop()