# home_view.py
import customtkinter

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
        self.bordered_box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=10)
        self.bordered_box.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        
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

        # Add a label inside the notifications box
        self.notifications_label = customtkinter.CTkLabel(
            self.notifications_box, text="Notificaciones", text_color="#114C5F"
        )
        self.notifications_label.pack(padx=10, pady=10)

        # Add a label for pH alert
        self.ph_alert_label = customtkinter.CTkLabel(
            self.notifications_box, text="⚠️ pH bajo detectado", text_color="#FF0000"
        )
        self.ph_alert_label.pack(padx=10, pady=(5, 10))

        # Add a label for nutrient alert
        self.nutrient_alert_label = customtkinter.CTkLabel(
            self.notifications_box,
            text="⚠️ Nutrientes insuficientes",
            text_color="#FF0000",
        )
        self.nutrient_alert_label.pack(padx=10, pady=(5, 10))
        
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
            text="0.94 S/m",
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
            text="7.2 ph",
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

        # Etiqueta para el valor (27 °C) con tamaño aumentado y en negrita
        self.temp_value_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text="27 °C",
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
            text="30",
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
