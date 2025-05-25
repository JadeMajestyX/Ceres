import customtkinter
from PIL import Image
import os
from utils.functions.functions import get_status_actuador, update_status_actuador, upadate_tiempo_bomba, update_tiempo_bomba_on
from config.security import check_password

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
        # Obtener estado inicial usando get_status_actuador

        if(title == "Nivel de Agua"):
            nombre_actuador = "bomba"
        elif(title == "Conductividad Eléctrica"):
            nombre_actuador = "solucion"
        elif(title == "pH"):
            nombre_actuador = "ph"

        estado_inicial = get_status_actuador(nombre_actuador)  # True o False

        if estado_inicial == "True":
            estado_inicial = True
        elif estado_inicial == "False":
            estado_inicial = False

        switch_btn = customtkinter.CTkButton(
            box,
            image=on_img if estado_inicial else off_img,
            text="",
            fg_color="#9CD2D3",
            hover_color="#9CD2D3",
            width=100,
            height=60,
        )
        switch_btn.is_on = estado_inicial  # Asignar atributo aquí

        # Luego asignar el comando que lo use
        switch_btn.configure(command=lambda btn=switch_btn, name=nombre_actuador: self.toggle_actuator(btn, name, on_img, off_img))

        switch_btn.grid(row=0, column=3, padx=10, pady=0)





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
        win.geometry("600x300")
        win.lift()
        win.grab_set()
        win.focus_force()

        ConfigOptions(win, actuator_name=title).pack(fill="both", expand=True)

    def toggle_actuator(self, switch_btn, actuator_name, on_img, off_img):
        if switch_btn.is_on:
            # Intentar apagar → requiere contraseña
            if not check_password():
                return  # No hacer nada si la contraseña es incorrecta

        # Cambiar el estado
        switch_btn.is_on = not switch_btn.is_on
        # Actualizar imagen
        switch_btn.configure(image=on_img if switch_btn.is_on else off_img)
        # Actualizar estado en base de datos o archivo
        estado = "encendido" if switch_btn.is_on else "apagado"
        print(f"{actuator_name} {estado}")
        new = "True" if estado == "encendido" else "False"
        update_status_actuador(actuator_name, new)





class ConfigOptions(customtkinter.CTkFrame):
    def __init__(self, master, actuator_name="", *args, **kwargs):
        super().__init__(master, fg_color="#114C5F", *args, **kwargs)
        self.master = master
        self.actuator_name = actuator_name
        self.calibration_sliders = []
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.abspath(os.path.join(base, '..', '..', 'assets', 'images'))

        customtkinter.CTkLabel(
            self,
            text="Configuración de Actuador",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(pady=(20, 10))

        if self.actuator_name.lower() != "nivel de agua":
            # Mensaje informativo común
            customtkinter.CTkLabel(
                self,
                text="Se necesita que las bombas peristálticas suministren 1ml.",
                font=("Arial", 14),
                text_color="white",
                wraplength=550,
                justify="center"
            ).pack(pady=(0, 10))

        # Solo para "Nivel de Agua"
        if self.actuator_name.lower() == "nivel de agua":
            # Mensaje específico para Nivel de Agua
            customtkinter.CTkLabel(
                self,
                text="Configura el intervalo de activación de la bomba de agua según el nivel detectado.",
                font=("Arial", 14),
                text_color="white",
                wraplength=550,
                justify="center"
            ).pack(pady=(0, 10))

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

        else:
            self.interval = None
            self.create_calibration_section()  # Solo si no es "Nivel de Agua"

        # Botón Guardar
        save_path = os.path.join(self.icon_dir, "SaveIcon.png")
        try:
            pil_save = Image.open(save_path).convert("RGBA")
            save_img = customtkinter.CTkImage(light_image=pil_save, size=(24, 24))
        except Exception as e:
            print(f"Error cargando icono de guardar {save_path}: {e}")
            save_img = None

        customtkinter.CTkButton(
            self,
            text="Guardar",
            image=save_img,
            compound="left",
            fg_color="#F18F01",
            hover_color="#D17E00",
            width=180,
            height=40,
            command=self.save_settings
        ).pack(pady=20)

    def create_calibration_section(self):
        # Determinar cuántos sliders necesita este actuador
        if self.actuator_name.lower() == "conductividad eléctrica":
            count = 3
        elif self.actuator_name.lower() == "ph":
            count = 2
        else:
            count = 1

        frame_c = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_c.pack(padx=20, pady=(0, 20), fill="x")

        for i in range(count):
            frame_c.grid_columnconfigure(i * 3 + 1, weight=1)

            label = customtkinter.CTkLabel(
                frame_c,
                text=f"Calibración Bomba {i+1}:" if count > 1 else "Calibración:",
                text_color="white"
            )
            label.grid(row=i, column=0, padx=(0,10), pady=5)

            slider = customtkinter.CTkSlider(
                frame_c,
                from_=0.1,
                to=1.0,
                number_of_steps=9,
                command=lambda val, idx=i: self.update_calibration_value(val, idx)
            )
            slider.set(0.5)
            slider.grid(row=i, column=1, sticky="ew", pady=5)

            val_label = customtkinter.CTkLabel(
                frame_c,
                text=f"{slider.get():.2f}",
                text_color="white"
            )
            val_label.grid(row=i, column=2, padx=(10, 0))

            self.calibration_sliders.append((slider, val_label))


    def update_calibration_value(self, value, idx):
        self.calibration_sliders[idx][1].configure(text=f"{float(value):.2f}")

    def save_settings(self):
        calibraciones = [s.get() for s, _ in self.calibration_sliders]
        intervalo = self.interval.get() if self.interval else "N/A"
        print(f"Guardando - Calibraciones: {calibraciones}, Intervalo: {intervalo}")
        if intervalo == "Siempre":
            tiempo = 0
            upadate_tiempo_bomba(0)
            update_tiempo_bomba_on(60000)
        elif intervalo == "10 minutos":
            tiempo = 10
            upadate_tiempo_bomba(600)
            update_tiempo_bomba_on(600)
        elif intervalo == "30 minutos":
            tiempo = 30
            upadate_tiempo_bomba(1800)
            update_tiempo_bomba_on(1800)



if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    root = customtkinter.CTk()
    root.geometry("1200x900")
    root.title("Vista de Actuadores")
    ActuatorsView(root).pack(fill="both", expand=True)
    root.mainloop()