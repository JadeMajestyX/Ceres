import customtkinter
from PIL import Image, ImageTk
import os
import platform
from tkinter import messagebox

def Windows11Notification(master, title, message, duration=5000):
    """Muestra una alerta estándar usando messagebox de tkinter"""
    messagebox.showinfo(title, message, parent=master)

class ActuatorsView(customtkinter.CTkFrame):
    """
    Vista de Actuadores con notificaciones estilo Windows 11
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="#114C5F")  # Fondo principal azul oscuro
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
            ("Conductividad Eléctrica", "CE.png", "#A6F0FF",  # Azul claro celeste
             "Los actuadores activan bombas dosificadoras para ajustar la concentración de nutrientes cuando la CE está fuera del rango ideal."),
            ("pH", "ph.png", "#B2CDFF",  # Azul lila claro
             "Se usan bombas para añadir soluciones ácidas o básicas y mantener el pH dentro del nivel óptimo para las plantas."),
            ("Temperatura", "Temp.png", "#87E2FF",  # Azul cielo
             "Ventiladores o calentadores se activan automáticamente para regular la temperatura del agua o ambiente."),
            ("Nivel de Agua", "LW.png", "#FFF8E9",  # Blanco amarillento
             "Una bomba se activa cuando el nivel de agua baja, asegurando que siempre haya suficiente líquido para las raíces."),
        ]
        for idx, (title, ico, icon_color, desc) in enumerate(actuators):
            icon_path = os.path.join(self.icon_dir, ico)
            self.create_actuator_box(idx, title, icon_path, desc, icon_color)

    def create_actuator_box(self, row, title, icon_path, description, icon_color):
        """Crea una fila con columnas de ancho adaptable y contenido centrado"""
        # Frame principal del actuador - Cambiado a color verde azulado claro
        box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=15)
        box.grid(row=row, column=0, padx=25, pady=15, sticky="nsew")

        # Configurar columnas
        col_weights = [4, 3, 2, 3, 2]
        for i, weight in enumerate(col_weights):
            box.grid_columnconfigure(i, weight=weight, uniform="col")
        box.grid_rowconfigure(0, weight=1)

        # Título - Cambiado a gris oscuro
        lbl_title = customtkinter.CTkLabel(
            box,
            text=title,
            font=("Arial", 22, "bold"),
            text_color="#393939",  # Gris oscuro
            wraplength=300,
            justify="center"
        )
        lbl_title.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)

        # Icono con fondo circular del color específico para cada actuador
        try:
            img = customtkinter.CTkImage(
                light_image=Image.open(icon_path), size=(60, 60)
            )
        except Exception as e:
            print(f"Error cargando icono {icon_path}: {e}")
            img = None
        
        # Fondo circular para el icono - Usamos el color específico del actuador
        icon_frame = customtkinter.CTkFrame(box, fg_color=icon_color, corner_radius=30, width=70, height=70)
        icon_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        icon_frame.grid_propagate(False)
        icon_frame.grid_rowconfigure(0, weight=1)
        icon_frame.grid_columnconfigure(0, weight=1)
        
        lbl_icon = customtkinter.CTkLabel(icon_frame, image=img, text="")
        lbl_icon.grid(row=0, column=0, sticky="nsew")

        # Botón de información - Azul más oscuro
        info_frame = customtkinter.CTkFrame(box, fg_color="transparent")
        info_frame.grid(row=0, column=2, sticky="nsew")
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)
        
        info_btn = customtkinter.CTkButton(
            info_frame,
            text="ℹ️",
            font=("Arial", 16),
            fg_color="#408DA6",  # Azul medio
            hover_color="#2D6A8F",  # Azul más oscuro
            width=36,
            height=36,
            corner_radius=18,
            command=lambda desc=description, title=title: self.show_info_notification(title, desc)
        )
        info_btn.grid(row=0, column=0)

        # Switch ON/OFF - Verde para ON, rojo para OFF
        switch_frame = customtkinter.CTkFrame(box, fg_color="transparent")
        switch_frame.grid(row=0, column=3, sticky="nsew")
        switch_frame.grid_rowconfigure(0, weight=1)
        switch_frame.grid_columnconfigure(0, weight=1)
        
        switch = customtkinter.CTkSwitch(
            switch_frame,
            text="",
            progress_color="#4ADE80",  # Verde brillante para ON
            fg_color="#FF6B6B",  # Rojo para OFF
            button_color="white",
            button_hover_color="#F0F0F0",
            width=70,
            height=32
        )
        switch.grid(row=0, column=0, padx=5)

        # Botón de ajustes - Azul claro consistente
        btn_frame = customtkinter.CTkFrame(box, fg_color="transparent")
        btn_frame.grid(row=0, column=4, sticky="nsew")
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        btn = customtkinter.CTkButton(
            btn_frame,
            text="⚙️",
            font=("Arial", 16),
            fg_color="#00A3C4",  # Azul claro
            hover_color="#0089A3",  # Azul más oscuro
            width=44,
            height=44,
            corner_radius=22,
            command=lambda t=title: self.open_settings(t)
        )
        btn.grid(row=0, column=0, sticky="e", padx=8)

    def show_info_notification(self, title, description):
        """Muestra una notificación estilo Windows 11"""
        Windows11Notification(self, f"Información - {title}", description)

    def open_settings(self, title):
        """Abre modal de configuración para el actuador"""
        win = customtkinter.CTkToplevel(self)
        win.title(f"Configuración - {title}")
        win.geometry("650x450")
        win.resizable(False, False)

        # Mantener al frente
        win.lift()
        win.grab_set()
        win.focus_force()

        ConfigOptions(win, title).pack(fill="both", expand=True)

class ConfigOptions(customtkinter.CTkFrame):
    """Panel de configuración para actuadores"""
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, fg_color="#114C5F", *args, **kwargs)  # Fondo azul oscuro
        self.master = master
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        # Título con fondo azul claro
        header_frame = customtkinter.CTkFrame(self, fg_color="#00A3C4", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        lbl = customtkinter.CTkLabel(
            header_frame,
            text=f"Configuración de {self.title}",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        lbl.pack(pady=20)

        # Contenedor principal - Azul medio
        main_frame = customtkinter.CTkFrame(self, fg_color="#0089A3", corner_radius=15)
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Intervalo
        frame_i = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        frame_i.pack(padx=20, pady=25, fill="x")
        
        customtkinter.CTkLabel(
            frame_i, 
            text="Intervalo:", 
            text_color="white",
            font=("Arial", 18)
        ).pack(side="left", padx=10)
        
        self.interval = customtkinter.CTkOptionMenu(
            frame_i,
            values=["10 minutos", "30 minutos", "1 hora", "2 horas", "Siempre"],
            fg_color="#408DA6",  # Azul medio
            button_color="#408DA6",
            dropdown_fg_color="#0089A3",  # Azul más oscuro
            width=180,
            height=40,
            font=("Arial", 16),
            dropdown_font=("Arial", 16)
        )
        self.interval.set("30 minutos")
        self.interval.pack(side="right", padx=10)

        # Días
        frame_d = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        frame_d.pack(padx=20, pady=25, fill="x")
        
        customtkinter.CTkLabel(
            frame_d, 
            text="Días:", 
            text_color="white",
            font=("Arial", 18)
        ).pack(side="left", padx=10)
        
        days_frame = customtkinter.CTkFrame(frame_d, fg_color="transparent")
        days_frame.pack(side="right", fill="x", expand=True)
        
        for i, d in enumerate(["L", "M", "X", "J", "V", "S", "D"]):
            chk = customtkinter.CTkCheckBox(
                days_frame, 
                text=d,
                width=30,
                height=30,
                checkbox_width=24,
                checkbox_height=24,
                corner_radius=5,
                border_width=2,
                fg_color="#4ADE80",  # Verde brillante
                hover_color="#3BC070",  # Verde más oscuro
                font=("Arial", 16, "bold")
            )
            if i < 5:  # Marcar días laborables por defecto
                chk.select()
            chk.grid(row=0, column=i, padx=12)
            days_frame.grid_columnconfigure(i, weight=1)

        # Botones
        btn_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30, fill="x")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        btn_cancel = customtkinter.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#6C757D",  # Gris
            hover_color="#5A6268",  # Gris más oscuro
            width=120,
            height=36,
            font=("Arial", 14, "bold"),
            corner_radius=8,
            command=self.master.destroy
        )
        btn_cancel.grid(row=0, column=0, padx=20)
        
        btn_save = customtkinter.CTkButton(
            btn_frame,
            text="Guardar",
            fg_color="#F18F01",  # Naranja
            hover_color="#D17E00",  # Naranja más oscuro
            width=120,
            height=36,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        btn_save.grid(row=0, column=1, padx=20)

if __name__ == "__main__":
    # Configuración inicial
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")
    
    # Crear ventana principal
    root = customtkinter.CTk()
    root.geometry("1200x900")
    root.title("Control de Actuadores - Sistema Hidropónico")
    
    # Vista principal
    ActuatorsView(root).pack(fill="both", expand=True, padx=20, pady=20)
    
    # Iniciar aplicación
    root.mainloop()