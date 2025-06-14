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
        
        # Botón para intervalo de 30 minutos
        self.btn_30min = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="30 Min",
            width=80,
            command=lambda: self.set_measurement_interval(0.5)
        )
        self.btn_30min.pack(side="left", padx=5, pady=5)
        
        # Botón para intervalo de 12 horas
        self.btn_12h = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="12 Horas",
            width=80,
            command=lambda: self.set_measurement_interval(12)
        )
        self.btn_12h.pack(side="left", padx=5, pady=5)
        
        # Botón para intervalo de 24 horas
        self.btn_24h = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="24 Horas",
            width=80,
            command=lambda: self.set_measurement_interval(24)
        )
        self.btn_24h.pack(side="left", padx=5, pady=5)
        
        # Botón para intervalo de 1 semana
        self.btn_1week = customtkinter.CTkButton(
            button_frame,
            fg_color="#408DA6",
            text="1 Semana",
            width=80,
            command=lambda: self.set_measurement_interval(168)
        )
        self.btn_1week.pack(side="left", padx=5, pady=5)
        
        # Establecer estilo para el botón activo
        self.active_button = None
        self.set_active_button(self.btn_24h)
        self.top_padding = 60

    def set_measurement_interval(self, hours):
        """Cambia el intervalo de medición y actualiza las gráficas"""
        if hours == 0.5:
            self.set_active_button(self.btn_30min)
        elif hours == 12:
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
                if hours == 0.5: 
                    points, interval = 12, 0.5  
                elif hours == 12:
                    points, interval = 12, 1
                elif hours == 24:
                    points, interval = 24, 1
                else:  
                    points, interval = 7, 24
                
                time_labels = self.generate_time_data(points, interval)
                min_val, max_val = config["y_range"]
                values = [random.uniform(min_val*1.05, max_val*0.95) for _ in range(points)]
                
                # Almacenar datos para la vista expandida
                setattr(self, f"{sensor}_graph_data", (time_labels, values))
                
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
        
        # Frame superior para icono y botón de expansión
        top_frame = customtkinter.CTkFrame(box, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=0)
        
        # Icono
        self.create_icon(top_frame, icon_path, sub_color)
        
        # Cargar imagen para el botón de expansión
        expand_icon = customtkinter.CTkImage(
            light_image=Image.open("assets/images/expandir.png"),
            dark_image=Image.open("assets/images/expandir.png"),
            size=(20, 20)  # Ajusta el tamaño según tu diseño
        )

        # Botón de expansión con imagen
        expand_btn = customtkinter.CTkButton(
            top_frame,
            image=expand_icon,
            text="",  # Sin texto
            width=30,
            height=30,
            fg_color=sub_color,
            hover_color="#80B0B9",
            command=lambda t=title, lc=line_color, fc=fill_color, yr=y_range,
                           u=unit, rl=reference_line: self.show_expanded_graph(t, lc, fc, yr, u, rl)
        )
        expand_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ne")
        
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
        setattr(self, f"{title.split()[0].lower()}_graph_data", (time_labels, values))
        
        # Etiqueta inferior
        self.create_bottom_label(box, title, sub_color)

    def show_expanded_graph(self, title, line_color, fill_color, y_range, unit, reference_line):
        """Muestra la gráfica en un modal expandido"""
        # Crear ventana modal
        modal = customtkinter.CTkToplevel(self)
        modal.title(f"Gráfica detallada: {title}")
        modal.geometry("1000x500")
        modal.grab_set()  # Hace el modal modal
        
        # Configurar grid
        modal.grid_rowconfigure(0, weight=1)
        modal.grid_columnconfigure(0, weight=1)
        
        # Obtener datos de la gráfica
        sensor_key = title.split()[0].lower()
        time_labels, values = getattr(self, f"{sensor_key}_graph_data")
        
        # Frame para la gráfica
        graph_frame = customtkinter.CTkFrame(modal, fg_color="#9CD2D3", corner_radius=10)
        graph_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)
        
        # Crear gráfica expandida
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100, facecolor='#8FC1C2')
        
        # Dibujar gráfica
        ax.plot(time_labels, values, color=line_color, linewidth=3)
        ax.fill_between(time_labels, values, y_range[0], color=fill_color, alpha=0.3)
        
        # Añadir anotaciones para los picos
        peaks = self.find_peaks(values)
        for i in peaks:
            ax.annotate(f'{values[i]:.2f}{unit}',
                    xy=(i, values[i]),
                    xytext=(0, 15),
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    fontsize=12,
                    color='#2E4053',
                    bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='white',
                                edgecolor='none',
                                alpha=0.7))
        
        # Configurar estilos
        self.style_expanded_graph(ax, fig, unit, y_range, reference_line)
        
        # Integrar gráfica en el modal
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botón de cerrar
        close_btn = customtkinter.CTkButton(
            modal,
            text="Cerrar",
            command=modal.destroy,
            fg_color="#F18F01",
            hover_color="#AB6500",
            width=100
        )
        close_btn.grid(row=1, column=0, pady=(0, 20))

    def style_expanded_graph(self, ax, fig, unit, y_range, reference_line):
        """Estilo para la gráfica expandida"""
        ax.set_facecolor('#8FC1C2')
        fig.set_facecolor('#8FC1C2')
        ax.set_ylabel(unit, fontsize=16, color='#2E4053', labelpad=15)
        ax.set_ylim(y_range)
        
        # Configurar ticks del eje X para mostrarlos en la vista expandida
        ax.tick_params(
            axis='x',
            which='both',
            labelsize=12,
            colors='#2E4053',
            rotation=45
        )
        
        ax.tick_params(
            axis='y',
            which='major',
            labelsize=14,
            colors='#2E4053',
            pad=10
        )
        
        # Cuadrícula
        ax.grid(
            True,
            linestyle='--',
            alpha=0.3,
            color='#FFFFFF'
        )
        
        # Línea de referencia
        ax.axhline(
            y=reference_line,
            color='#F18F01',
            linestyle='--',
            linewidth=2,
            alpha=0.7
        )
        
        # Eliminar bordes
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        fig.set_constrained_layout(True)

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
        if interval < 1:  # Para minutos
            return [(now - timedelta(minutes=int(i*interval*60))).strftime('%H:%M') 
                    for i in range(points, 0, -1)]
        elif interval == 1:  # Horas exactas
            return [(now - timedelta(hours=i)).strftime('%H:%M') 
                    for i in range(points, 0, -1)]
        else:  # Días
            return [(now - timedelta(hours=i*interval)).strftime('%d/%m') 
                    for i in range(points, 0, -1)]

    def create_fill_between_graph(self, master, times, values, line_color, fill_color, y_range, unit, reference_line):
        """Crea gráficas con valores exactos en los picos"""
        plt.close('all')
        # Crear figura
        fig, ax = plt.subplots(
            figsize=(5, 3),
            dpi=80,
            facecolor='#8FC1C2',
            constrained_layout=True
        )
        # Asegurar referencia visible
        ref_line = max(y_range[0], min(y_range[1], reference_line))
        
        # Dibujar gráfica
        line, = ax.plot(times, values, color=line_color, linewidth=2.5)
        ax.fill_between(times, values, y_range[0], color=fill_color, alpha=0.2)
        # Encontrar picos locales (máximos y mínimos)
        peaks = self.find_peaks(values)
        # Añadir anotaciones para los picos
        for i in peaks:
            ax.annotate(f'{values[i]:.2f}{unit}',
                    xy=(i, values[i]),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    fontsize=12,
                    color='#2E4053',
                    bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='white',
                                edgecolor='none',
                                alpha=0.7))
        # Aplicar estilos
        self.style_graph(ax, fig, unit, y_range, ref_line)
        # Integrar gráfica
        self.embed_graph(fig, master)

    def find_peaks(self, values, threshold=0.1):
        """Encuentra los picos (máximos y mínimos locales) en los datos"""
        peaks = []
        for i in range(1, len(values)-1):
            # Máximo local
            if values[i] > values[i-1] and values[i] > values[i+1]:
                peaks.append(i)
            # Mínimo local
            elif values[i] < values[i-1] and values[i] < values[i+1]:
                peaks.append(i)
        # Si no hay suficientes picos, mostramos algunos puntos clave
        if len(peaks) < 3:
            peaks = []
            step = max(1, len(values) // 3)
            for i in range(0, len(values), step):
                peaks.append(i)
            peaks.append(len(values)-1)  # Asegurar el último punto
        return peaks

    def style_graph(self, ax, fig, unit, y_range, reference_line):
        """Configura todos los estilos visuales de la gráfica"""
        # Configuración previa (igual que antes)
        ax.set_facecolor('#8FC1C2')
        fig.set_facecolor('#8FC1C2')
        ax.set_ylabel(unit, fontsize=16, color='#2E4053', labelpad=10)
        ax.set_ylim(y_range)
        # Configuración de ticks
        ax.tick_params(
            axis='y',
            which='major',
            labelsize=12,
            colors='#2E4053',
            pad=5
        )
        ax.tick_params(
            axis='x',
            which='both',
            bottom=False,
            labelbottom=False
        )
        # Cuadrícula
        ax.grid(
            True,
            linestyle='--',
            alpha=0.3,
            color='#FFFFFF'
        )
        # Línea de referencia
        ax.axhline(
            y=reference_line,
            color='#F18F01',
            linestyle='--',
            linewidth=1.5,
            alpha=0.7
        )
        
        # Eliminar bordes del gráfico
        for spine in ax.spines.values():
            spine.set_visible(False)
        # Ajuste automático de layout
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
            font=("Arial", 16, "bold"),
            text_color="#393939",
            anchor="center"
        )
        sub_label.grid(row=0, column=0, sticky="")