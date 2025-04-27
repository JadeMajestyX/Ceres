import customtkinter
import matplotlib.pyplot as plt
from PIL import Image
from customtkinter import CTkImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime, timedelta

class SensoresView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#114C5F")       
        # Configuración del grid principal
        self.configure_grid()
        # Añadir botones de intervalo de medición
        self.add_measurement_buttons()
        # Crear contenedores para cada sensor
        self.create_sensor_containers()

    def configure_grid(self):
        """Configura el grid principal"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def add_measurement_buttons(self):
        """Añade los botones de intervalo de medición en la parte superior derecha"""
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)       
        # Botón para intervalo de 12 horas
        self.btn_12h = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="12 Horas",
            width=100,
            command=lambda: self.set_measurement_interval(12)
        )
        self.btn_12h.pack(side="left", padx=5, pady=5)       
        # Botón para intervalo de 24 horas
        self.btn_24h = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="24 Horas",
            width=100,
            command=lambda: self.set_measurement_interval(24)
        )
        self.btn_24h.pack(side="left", padx=5, pady=5)        
        # Botón para intervalo de 1 semana
        self.btn_1week = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="1 Semana",
            width=100,
            command=lambda: self.set_measurement_interval(168)
        )
        self.btn_1week.pack(side="left", padx=5, pady=5)        
        # Establecer estilo para el botón activo
        self.active_button = None
        self.set_active_button(self.btn_24h)
        self.top_padding = 60

    def set_measurement_interval(self, hours):
        """Cambia el intervalo de medición y actualiza las gráficas"""
        if hours == 12:
            self.set_active_button(self.btn_12h)
        elif hours == 24:
            self.set_active_button(self.btn_24h)
        elif hours == 168:
            self.set_active_button(self.btn_1week)       
        self.update_all_graphs(hours)

    def set_active_button(self, button):
        """Resalta el botón del intervalo activo"""
        if self.active_button:
            self.active_button.configure(fg_color="#408DA6")
        self.active_button = button
        button.configure(fg_color="#F18F01")

    def update_all_graphs(self, hours):
        """Actualiza todas las gráficas con el nuevo intervalo"""
        plt.close('all')  # Cerrar todas las figuras anteriores        
        for sensor in ["conductividad", "acidez", "temperatura", "nivel"]:
            graph_frame = getattr(self, f"{sensor}_graph_frame", None)
            if graph_frame:
                # Limpieza exhaustiva del frame
                for widget in graph_frame.winfo_children():
                    widget.destroy()
                if hasattr(graph_frame, '_current_canvas'):
                    graph_frame._current_canvas.get_tk_widget().destroy()                
                # Obtener configuración del sensor
                config = self.get_sensor_config(sensor)
                
                # Generar datos según el intervalo
                if hours == 12:
                    points, interval = 12, 1
                elif hours == 24:
                    points, interval = 24, 1
                else:  # 1 semana
                    points, interval = 7, 24                
                time_labels = self.generate_time_data(points, interval)
                min_val, max_val = config["y_range"]
                values = [random.uniform(min_val*1.05, max_val*0.95) for _ in range(points)]               
                # Crear nueva gráfica
                self.create_fill_between_graph(
                    master=graph_frame,
                    times=time_labels,
                    values=values,
                    **config
                )

    def get_sensor_config(self, sensor_type):
        """Devuelve la configuración para cada tipo de sensor"""
        config = {
            "conductividad": {
                "line_color": "#A6F0FF",
                "fill_color": "#2E86AB",
                "y_range": (0.0, 4.0),
                "unit": "mS/cm",
                "reference_line": 2.5
            },
            "acidez": {
                "line_color": "#B2CDFF",
                "fill_color": "#A23B72",
                "y_range": (2, 10),
                "unit": "pH",
                "reference_line": 6.0
            },
            "temperatura": {
                "line_color": "#87E2FF",
                "fill_color": "#114C5F",
                "y_range": (18, 27),
                "unit": "°C",
                "reference_line": 22
            },
            "nivel": {
                "line_color": "#FFF8E9",
                "fill_color": "#3B1F2B",
                "y_range": (0, 50),
                "unit": "%",
                "reference_line": 30
            }
        }
        return config.get(sensor_type.lower(), {})

    def create_sensor_containers(self):
        """Crea los 4 contenedores de sensores"""
        # Conductividad eléctrica
        self.create_sensor_box(
            row=0, column=0,
            title="Conductividad eléctrica",
            icon_path="assets/images/CE.png",
            bg_color="#9CD2D3",
            sub_color="#A6F0FF",
            line_color="#A6F0FF",
            fill_color="#2E86AB",
            y_range=(0.0, 4.0),
            unit="mS/cm",
            reference_line=2.5,
            pad_y=(self.top_padding, 20)
        )       
        # Nivel de pH
        self.create_sensor_box(
            row=0, column=1,
            title="Acidez o Alcalinidad",
            icon_path="assets/images/ph.png",
            bg_color="#9CD2D3",
            sub_color="#B2CDFF",
            line_color="#B2CDFF",
            fill_color="#A23B72",
            y_range=(2, 10),
            unit="pH",
            reference_line=6.0,
            pad_y=(self.top_padding, 20)
        )       
        # Temperatura del agua
        self.create_sensor_box(
            row=1, column=0,
            title="Temperatura del agua",
            icon_path="assets/images/Temp.png",
            bg_color="#9CD2D3",
            sub_color="#87E2FF",
            line_color="#87E2FF",
            fill_color="#114C5F",
            y_range=(18, 27),
            unit="°C",
            reference_line=22,
            pad_y=(20, 20)
        )       
        # Nivel del agua
        self.create_sensor_box(
            row=1, column=1,
            title="Nivel del agua",
            icon_path="assets/images/LW.png",
            bg_color="#9CD2D3",
            sub_color="#FFF8E9",
            line_color="#FFF8E9",
            fill_color="#3B1F2B",
            y_range=(0, 50),
            unit="%",
            reference_line=30,
            pad_y=(20, 20)
        )

    def create_sensor_box(self, row, column, title, icon_path, bg_color, sub_color, line_color, fill_color, y_range, unit, reference_line, pad_y):
        """Crea un contenedor completo para cada sensor"""
        box = customtkinter.CTkFrame(self, fg_color=bg_color, corner_radius=10)
        box.grid(row=row, column=column, padx=(20, 20), pady=pad_y, sticky="nsew")       
        box.grid_rowconfigure(0, weight=0)
        box.grid_rowconfigure(1, weight=1)
        box.grid_rowconfigure(2, weight=0)
        box.grid_columnconfigure(0, weight=1)
        # Icono
        self.create_icon(box, icon_path, sub_color)        
        # Gráfica
        graph_frame = customtkinter.CTkFrame(box, fg_color="#9CD2D3", corner_radius=5)
        graph_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")       
        # Generar datos iniciales
        time_labels, values = self.generate_sample_data(y_range)        
        # Crear gráfica inicial
        self.create_fill_between_graph(
            master=graph_frame,
            times=time_labels,
            values=values,
            line_color=line_color,
            fill_color=fill_color,
            y_range=y_range,
            unit=unit,
            reference_line=reference_line
        )        
        # Almacenar referencia
        setattr(self, f"{title.split()[0].lower()}_graph_frame", graph_frame)       
        # Etiqueta inferior
        self.create_bottom_label(box, title, sub_color)

    def create_icon(self, parent, icon_path, bg_color):
        """Crea el icono del sensor"""
        try:
            icon = CTkImage(light_image=Image.open(icon_path), size=(40, 40))
            icon_frame = customtkinter.CTkFrame(
                parent, fg_color=bg_color, width=30, height=30, corner_radius=8
            )
            icon_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")           
            icon_label = customtkinter.CTkLabel(icon_frame, image=icon, text="")
            icon_label.pack(expand=True, fill="both", padx=5, pady=5)
        except Exception as e:
            print(f"Error cargando icono: {e}")

    def generate_sample_data(self, y_range, points=24):
        """Genera datos de ejemplo para la gráfica"""
        time_labels = self.generate_time_data(points)
        values = [random.uniform(y_range[0]*1.05, y_range[1]*0.95) for _ in range(points)]
        return time_labels, values

    def generate_time_data(self, points, interval=1):
        """Genera etiquetas de tiempo según el intervalo seleccionado"""
        now = datetime.now()
        return [(now - timedelta(hours=i*interval)).strftime('%H:%M' if interval == 1 else '%d/%m') 
                for i in range(points, 0, -1)]

    def create_fill_between_graph(self, master, times, values, line_color, fill_color, y_range, unit, reference_line):
        """Crea gráficas sin warnings con layout optimizado"""
        plt.close('all')       
        # Crear figura con constrained_layout
        fig, ax = plt.subplots(
            figsize=(5, 3),
            dpi=80,
            facecolor='#8FC1C2',
            constrained_layout=True  # Único sistema de layout
        )       
        # Asegurar referencia visible
        ref_line = max(y_range[0], min(y_range[1], reference_line))        
        # Dibujar gráfica
        ax.plot(times, values, color=line_color, linewidth=2.5)
        ax.fill_between(times, values, y_range[0], color=fill_color, alpha=0.2)       
        # Aplicar estilos
        self.style_graph(ax, fig, unit, y_range, ref_line)       
        # Integrar gráfica
        self.embed_graph(fig, master)

    def style_graph(self, ax, fig, unit, y_range, reference_line):
        """Configura todos los estilos visuales de la gráfica"""
        # 1. Configuración de colores de fondo
        ax.set_facecolor('#8FC1C2')    # Color del área de ploteo (donde están los datos)
        fig.set_facecolor('#8FC1C2')   # Color del fondo exterior (márgenes)       
        # 2. Configuración del eje Y
        ax.set_ylabel(unit, 
                    fontsize=12, 
                    color='#2E4053',  # Color texto eje Y
                    labelpad=10)      # Espaciado
        
        ax.set_ylim(y_range)  # Rango del eje Y       
        # 3. Configuración de ticks
        ax.tick_params(
            axis='y',
            which='major',
            labelsize=10,
            colors='#2E4053',  # Color de los números del eje Y
            pad=5              # Espaciado de los ticks
        )
        # Ocultar eje X
        ax.tick_params(
            axis='x',
            which='both',
            bottom=False,
            labelbottom=False
        )       
        # 4. Cuadrícula
        ax.grid(
            True,
            linestyle='--',
            alpha=0.3,
            color='#FFFFFF'  # Color de las líneas de grid (blanco semitransparente)
        )        
        # 5. Línea de referencia
        ax.axhline(
            y=reference_line,
            color='#F18F01',  # Color naranja para la línea de referencia
            linestyle='--',
            linewidth=1.5,
            alpha=0.7
        )       
        # 6. Texto de referencia
        ax.text(
            0.95, 0.95,  # Posición (95% del ancho/alto)
            f'Óptimo: {reference_line}{unit}',
            transform=ax.transAxes,  # Coordenadas relativas
            fontsize=10,
            color='#2E4053',
            va='top',
            ha='right',
            bbox=dict(
                facecolor='white',
                alpha=0.7,
                edgecolor='none',
                boxstyle='round,pad=0.3'  # Bordes redondeados
            )
        )       
        # 7. Eliminar bordes del gráfico
        for spine in ax.spines.values():
            spine.set_visible(False)        
        # 8. Ajuste automático de layout
        fig.set_constrained_layout(True)

    def embed_graph(self, fig, master):
        """Integra la gráfica en el frame"""
        # Limpiar frame primero
        for widget in master.winfo_children():
            widget.destroy()        
        # Crear y guardar canvas
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=2, pady=2)
        if hasattr(master, '_current_canvas'):
            master._current_canvas.get_tk_widget().destroy()
        master._current_canvas = canvas

    def create_bottom_label(self, parent, text, bg_color):
        """Crea la etiqueta inferior"""
        sub_frame = customtkinter.CTkFrame(
            parent, fg_color=bg_color, height=100, corner_radius=5
        )
        sub_frame.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")        
        sub_frame.grid_columnconfigure(0, weight=1)
        sub_frame.grid_rowconfigure(0, weight=1)        
        sub_label = customtkinter.CTkLabel(
            sub_frame,
            text=text,
            font=("Arial", 12, "bold"),
            text_color="#2E4053",
            anchor="center"
        )
        sub_label.grid(row=0, column=0, sticky="")