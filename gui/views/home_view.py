# home_view.py
import customtkinter
from PIL import Image  # Import PIL for image handling
import random
from models.medicionesModel import MedicionesModel
from utils.functions.functions import get_planta_id
import json

class HomeView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#114C5F")  # Establece el color de fondo

        # Configurar el sistema de pesos para que sea rescalable
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ###################################
        ### Recuadro superior izquierdo ###
        ###################################
        # Create a top-left bordered box with specified dimensions
        self.bordered_box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=15)
        self.bordered_box.grid(row=0, column=0, padx=(30, 15), pady=(30, 15), sticky="nsew")

        # Add a label to display the plant being cultivated
        self.plant_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Cultivo: Tomates",  # Replace "Tomates" with the actual plant name dynamically if needed
            font=("Arial", 28, "bold"),  # Larger font size
            text_color="#FFFFFF"  # White color for better contrast
        )
        self.plant_label.pack(padx=20, pady=(15, 10))

        # Add an image label to display the status
        self.status_image_label = customtkinter.CTkLabel(self.bordered_box, text="")
        self.status_image_label.pack(padx=20, pady=(10, 10))

        # Add a label to display the number of days the plant has been growing
        self.days_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Días de cultivo: 15",  # Replace "15" with the actual number of days dynamically if needed
            font=("Arial", 24, "bold"),  # Larger font size
            text_color="#114C5F"
        )
        self.days_label.pack(padx=20, pady=(10, 15))

        # Function to update the image based on values
        def update_status_image(values):
            if all(value == "good" for value in values):
                image = customtkinter.CTkImage(Image.open("icons/Muy bien.png"), size=(140, 140))
                self.status_image_label.configure(image=image)
            elif sum(1 for value in values if value == "bad") <= 2:
                image = customtkinter.CTkImage(Image.open("icons/maso menos.png"), size=(140, 140))
                self.status_image_label.configure(image=image)
            else:
                image = customtkinter.CTkImage(Image.open("icons/mal.png"), size=(140, 140))
                self.status_image_label.configure(image=image)

        # Replace these with actual logic to determine the status of each value
        example_values = ["good", "bad", "good", "bad"]
        update_status_image(example_values)
        #############################################
        ### Finzaliza Recuadro superior izquierdo ###
        ############################################# 

        #####################################
        #### Recuadro superior derecho ######
        #####################################

        # Create a top-right bordered box for notifications
        self.notifications_box = customtkinter.CTkFrame(
            self, fg_color="#9CD2D3", corner_radius=10
        )
        self.notifications_box.grid(
            row=0, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew"
        )

        # Configure grid weights for rescalability
        self.notifications_box.grid_rowconfigure(0, weight=1)
        self.notifications_box.grid_columnconfigure(0, weight=1)

        # Add a scrollable frame inside the notifications box
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.notifications_box, 
            fg_color="#9CD2D3", 
            corner_radius=10,
            width=350  # Ancho aumentado para las notificaciones
        )
        self.scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Add a label inside the scrollable frame
        self.notifications_label = customtkinter.CTkLabel(
            self.scrollable_frame, 
            text="Notificaciones", 
            text_color="#114C5F",
            font=("Arial", 16, "bold"),
            anchor="center"  # Centra el texto de la etiqueta
        )
        self.notifications_label.grid(row=0, column=0, padx=10, pady=(5, 15), sticky="ew")

        # Función para agregar notificaciones con el formato deseado
        def add_notification(text, severity="info"):
            notification_box = customtkinter.CTkFrame(
            self.scrollable_frame, 
            fg_color="#E0F7FA", 
            corner_radius=10
            )
            notification_box.grid(row=self.scrollable_frame.winfo_children().__len__(), column=0, padx=5, pady=5, sticky="ew")
            notification_box.grid_columnconfigure((0, 1), weight=1)

            # Determinar el color del icono según la severidad
            icon_color = "#114C5F"  # Azul por defecto
            if severity == "warning":
                icon_color = "#FFA500"  # Amarillo
            elif severity == "error":
                icon_color = "#FF0000"  # Rojo

            # Icono de información
            notification_icon = customtkinter.CTkLabel(
            notification_box,
            text="ℹ️" if severity == "info" else ("⚠️" if severity == "warning" else "❌"),
            font=("Arial", 16, "bold"),
            text_color=icon_color
            )
            notification_icon.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # Contenido de la notificación justificado y en una sola línea
            notification_content = customtkinter.CTkLabel(
            notification_box,
            text=text,
            text_color="#114C5F",
            font=("Arial", 14),
            anchor="w"  # Alinea el texto a la izquierda
            )
            notification_content.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Agregar notificaciones de ejemplo
        add_notification("Temperatura 2°C más alta de lo establecido.", severity="warning")
        add_notification("pH bajo: 6.2 (fuera del rango óptimo 6.5-7.5).", severity="error")
        add_notification("Conductividad crítica: 1.8 S/m (rango óptimo: 0.5-1.5 S/m).", severity="error")
        add_notification("Nutrientes bajos - agregar solución nutritiva.", severity="info")
        add_notification("Fluctuación inusual en la temperatura nocturna.", severity="warning")
        add_notification("Nivel de agua bajo - rellene el tanque.", severity="error")

        ###########################################
        ### Finzaliza Recuadro superior derecho ###
        ###########################################

        #########################
        ### Recuadro inferior ###
        #########################
        # Create a bottom bordered box with specified dimensions
        self.bottom_bordered_box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=10)
        self.bottom_bordered_box.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew")

        # Configure the grid for the bottom bordered box
        self.bottom_bordered_box.grid_rowconfigure(0, weight=1)
        self.bottom_bordered_box.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ###########################
        ####  Caja Numero 1   #####
        ###########################

        # Add a bordered box inside the bottom bordered box (left side)
        self.inner_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box, 
            fg_color="#0799B6",  # Fondo blanco (como en la imagen)
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"  # Borde gris claro (más discreto que en tu versión original)
        )
        self.inner_bordered_box.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Configuración de grid (igual que antes)
        self.inner_bordered_box.grid_rowconfigure(0, weight=1)
        self.inner_bordered_box.grid_rowconfigure(1, weight=1)
        self.inner_bordered_box.grid_rowconfigure(2, weight=1)
        self.inner_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono (ajustado a colores de imagen)
        self.icon_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            text="⚡",
            font=("Arial", 36, "bold"),
            text_color="#C39C00"  # Verde azulado oscuro (como el texto de la imagen)
        )
        self.icon_label.grid(row=0, column=0, pady=(10, 5))

        # Valor principal (ajustado a colores de imagen)
        self.value_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            text= str(MedicionesModel().obtener_medicion(get_planta_id(), "ec")) + " S/m",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"  # Mismo color que el icono
        )
        self.value_label.grid(row=1, column=0, pady=(5, 5))

        # Título (ajustado a colores de imagen)
        self.title_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            text="Conductividad eléctrica",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"  # Mismo color que los demás textos
        )
        self.title_label.grid(row=2, column=0, pady=(5, 10))

        ################################
        ### Finzaliza Caja Numero 1 ####
        ################################

        ######################################
        ######   Inicia Caja Numero 2  #######
        ######################################

        self.additional_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box, 
            fg_color="#4A6EB0",  # Color de fondo ligeramente diferente al primero
            corner_radius=10,
            border_width=1,
            border_color="#B2D8D8"  # Mismo color de borde que el primero
        )
        self.additional_bordered_box.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.additional_bordered_box.grid_rowconfigure((0, 1, 2), weight=1)
        self.additional_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para la caja adicional (en vertical)
        self.ph_icon_label = customtkinter.CTkLabel(
            self.additional_bordered_box,
            text="💧",  # Icono de gota de agua
            font=("Arial", 48, "bold"),  # Tamaño más grande y en negrita
            text_color="#006666"  # Mismo color de texto que el primero
        )
        self.ph_icon_label.grid(row=0, column=0, pady=(10, 5))

        # Etiqueta para el valor (7.2 ph) con tamaño aumentado y en negrita
        self.ph_value_label = customtkinter.CTkLabel(
            self.additional_bordered_box,
            text= str(MedicionesModel().obtener_medicion(get_planta_id(), "ph")) + " ph",
            font=("Arial", 28, "bold"),  # Tamaño más grande y en negrita
            text_color="#FFFFFF"  # Mismo color de texto que el primero
        )
        self.ph_value_label.grid(row=1, column=0, pady=(5, 5))

        # Etiqueta para la descripción
        self.ph_title_label = customtkinter.CTkLabel(
            self.additional_bordered_box,
            text="Acidez o alcalinidad",
            font=("Arial", 14, "bold"),  # Tamaño más grande y en negrita
            text_color="#FFFFFF"
        )
        self.ph_title_label.grid(row=2, column=0, pady=(5, 10))

        #######################################
        ###### Finzaliza Caja Numero 2 ########
        #######################################

        ####################################
        ####### Inicia Caja Numero 3########
        ####################################

        self.center_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box,
            fg_color="#114C5F",  # Color de fondo intermedio entre los dos anteriores
            corner_radius=10,
            border_width=1,
            border_color="#B2D8D8"  # Mismo color de borde consistente
        )
        self.center_bordered_box.grid(row=0, column=2, padx=(10, 10), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.center_bordered_box.grid_rowconfigure((0, 1, 2), weight=1)
        self.center_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para la caja central (en vertical)
        self.temp_icon_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text="🌡️",  # Icono de termómetro
            font=("Arial", 48, "bold"),  # Tamaño más grande y en negrita
            text_color="#006666"  # Mismo esquema de colores
        )
        self.temp_icon_label.grid(row=0, column=0, pady=(10, 5))

        self.temp_value_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text= str(MedicionesModel().obtener_medicion(get_planta_id(), "temp")) + " °C",
            font=("Arial", 28, "bold"),  # Tamaño más grande y en negrita
            text_color="#FFFFFF"  # Mismo esquema de colores
        )
        self.temp_value_label.grid(row=1, column=0, pady=(5, 5))

        # Etiqueta para la descripción
        self.temp_title_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text="Temperatura del agua",
            font=("Arial", 14, "bold"),  # Tamaño más grande y en negrita
            text_color="#FFFFFF"
        )
        self.temp_title_label.grid(row=2, column=0, pady=(5, 10))

        #######################################
        ####### Finaliza Caja Numero 3 ########
        #######################################

        ########################################
        #######  Inicia Caja Numero 4  #########
        ########################################

        self.far_right_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box,
            fg_color="#D0B98D",  # Color de fondo ligeramente más oscuro para diferenciación visual
            corner_radius=10,
            border_width=1,
            border_color="#B2D8D8"  # Mantiene consistencia con los otros cuadros
        )
        self.far_right_bordered_box.grid(row=0, column=3, padx=(10, 20), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.far_right_bordered_box.grid_rowconfigure((0, 1, 2), weight=1)
        self.far_right_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para el nivel del agua
        self.water_level_icon = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            text="🚰",  # Icono de grifo de agua
            font=("Arial", 48, "bold"),
            text_color="#006666"  # Mismo esquema de colores
        )
        self.water_level_icon.grid(row=0, column=0, pady=(10, 5))

        # Etiqueta para el valor (30)
        self.water_level_value = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            text=str(int(MedicionesModel().obtener_medicion(get_planta_id(), "water"))) + " %",
            font=("Arial", 28, "bold"),  # Negrita
            text_color="#FFFFFF"  # Mismo esquema de colores
        )
        self.water_level_value.grid(row=1, column=0, pady=(5, 5))


        # Etiqueta para la descripción
        self.water_level_title = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            text="Nivel del agua",
            font=("Arial", 14, "bold"),  # Negrita
            text_color="#FFFFFF"
        )
        self.water_level_title.grid(row=2, column=0, pady=(5, 10))

        ##########################################
        #######  Finaliza Caja Numero 4  #########
        ##########################################

        ##################################
        ### Finaliza Recuadro inferior ###
        ##################################