import customtkinter
from PIL import Image  # Import PIL for image handling
from models.medicionesModel import MedicionesModel
from utils.functions.functions import get_planta_id, nivel_de_agua, tiempo, get_dato_planta
from models.alertasModel import AlertasModel
from models.plantasModel import PlantasModel

class HomeView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#114C5F")  # Establece el color de fondo

        # Configurar el sistema de pesos para que sea rescalable
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Listas de severidades
        self.errors = [
            "No se detectó el Arduino",
            "Los datos del Arduino son incorrectos",
            "No se recibieron datos del Arduino",
            "No esta fluyendo el agua",
            "Los niveles de pH son demasiado altos",
            "Los niveles de pH son demasiado bajos",
            "La temperatura del agua es demasiado alta",
            "La temperatura del agua es demasiado baja",
            "La conductividad es demasiado alta",
            "La conductividad es demasiado baja",
            "El nivel de agua es demasiado bajo",
            "No se detecto el sensor de pH",
            "No se detecto el sensor de temperatura",
            "No se detecto el sensor de conductividad",
            "No se detecto el sensor de nivel de agua",
            "No se detecto el sensor de flujo",
            "No hay agua"
        ]

        self.warnings = [
            "El nivel de agua es bajo",
            "El nivel de agua es alto",
            "El pH es bajo",
            "El pH es alto",
            "El agua está fría",
            "El agua está caliente",
            "La conductividad es baja",
            "La conductividad es alta",
            "La temperatura del agua es alta",
            "La temperatura del agua es baja",
        ]
        self.infos = [
            "Se recomienda calibrar el sensor de pH",
            "Se recomienda calibrar el sensor de conductividad",
            "Se recomienda mover el sensor de nivel de agua",
        ]

        ###################################
        ### Recuadro superior izquierdo ###
        ###################################
        # Create a top-left bordered box with specified dimensions
        # Create a top-left bordered box with specified dimensions
        self.bordered_box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=15)
        self.bordered_box.grid(row=0, column=0, padx=(30, 15), pady=(30, 15), sticky="nsew")

        # Add a label to display the plant being cultivated
        self.plant_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Cultivo: " + get_dato_planta(get_planta_id(), "nombre"),
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        )
        self.plant_label.pack(padx=20, pady=(15, 10))

        # Add an image label to display the status
        self.status_image_label = customtkinter.CTkLabel(self.bordered_box, text="")
        self.status_image_label.pack(padx=20, pady=(10, 10))

        # Add a label to display the number of days the plant has been growing
        self.days_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Días de cultivo: " + str(tiempo()),
            font=("Arial", 24, "bold"),
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

        #####################################
        #### Recuadro superior derecho ######
        #####################################

        # Caja principal de notificaciones
        self.notifications_box = customtkinter.CTkFrame(
            self, fg_color="#9CD2D3", corner_radius=10
        )
        self.notifications_box.grid(
            row=0, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew"
        )

        self.notifications_box.grid_rowconfigure(0, weight=1)
        self.notifications_box.grid_columnconfigure(0, weight=1)

        # Marco desplazable
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.notifications_box,
            fg_color="#9CD2D3",
            corner_radius=10,
            width=350
        )
        self.scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Título
        self.title_frame = customtkinter.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 0))
        self.title_frame.grid_columnconfigure(0, weight=1)

        self.notifications_label = customtkinter.CTkLabel(
            self.title_frame,
            text="Notificaciones",
            text_color="#114C5F",
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        self.notifications_label.grid(row=0, column=0, sticky="w")

        # Lista de widgets de notificación
        self.notification_widgets = []  # [(frame, icon_label, content_label)]

        # Muestra detalle con recomendación
        def mostrar_info(texto, recomendacion):
            import tkinter.messagebox as messagebox
            mensaje = f"{texto}\n\n🛠 Recomendación:\n{recomendacion or 'Sin recomendaciones específicas.'}"
            messagebox.showinfo("Detalle de notificación", mensaje)

        # Crea y retorna el widget de notificación
        def add_notification_widget(text, severity="info", recomendacion=""):
            frame = customtkinter.CTkFrame(
            self.scrollable_frame,
            fg_color="#E0F7FA",
            corner_radius=10
            )
            frame.grid_columnconfigure((0, 1, 2), weight=1)

            icon_label = customtkinter.CTkLabel(
            frame,
            text="ℹ️" if severity == "info" else ("⚠️" if severity == "warning" else "❌"),
            font=("Arial", 16, "bold"),
            text_color=("#114C5F" if severity == "info" else ("#FFA500" if severity == "warning" else "#FF0000"))
            )
            icon_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            content_label = customtkinter.CTkLabel(
            frame,
            text=text,
            text_color="#114C5F",
            font=("Arial", 14),
            anchor="w"
            )
            content_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            info_button = customtkinter.CTkButton(
            frame,
            text="ℹ️",
            width=30,
            height=28,
            fg_color="#D0EBF4",
            hover_color="#B0D6E0",
            text_color="#114C5F",
            font=("Arial", 12),
            command=lambda: mostrar_info(text, recomendacion)
            )
            info_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

            return frame, icon_label, content_label

        # Carga y muestra notificaciones de ejemplo
        def cargar_notificaciones_ejemplo():
            ejemplos = [
            {"mensaje": "El nivel de agua es bajo", "severidad": "warning", "recomendacion": "Revisar el suministro de agua."},
            {"mensaje": "El pH es alto", "severidad": "error", "recomendacion": "Agregar solución para reducir el pH."},
            {"mensaje": "Sensor de temperatura requiere calibración", "severidad": "info", "recomendacion": "Calibrar el sensor de temperatura."}
            ]

            # Eliminar notificaciones anteriores
            for widget in self.notification_widgets:
                widget[0].destroy()
            self.notification_widgets.clear()

            # Crear y mostrar nuevas notificaciones
            for idx, ejemplo in enumerate(ejemplos):
                texto = ejemplo["mensaje"]
                severidad = ejemplo["severidad"]
                recomendacion = ejemplo.get("recomendacion", "")
                frame, icon_label, content_label = add_notification_widget(texto, severidad, recomendacion)
                frame.grid(row=idx + 1, column=0, padx=5, pady=5, sticky="ew")
                self.notification_widgets.append((frame, icon_label, content_label))

        # Cargar notificaciones de ejemplo al inicio
        cargar_notificaciones_ejemplo()

        ###########################################
        ### Fin del recuadro de notificaciones   ###
        ###########################################





        # (resto de la vista inferior permanece igual)

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

        # Icono (usando una imagen en lugar de texto)
        self.icon_image = customtkinter.CTkImage(Image.open("icons/2.png"), size=(72, 72))  # Tamaño aumentado
        self.icon_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            image=self.icon_image,
            text=""
        )
        self.icon_label.grid(row=0, column=0, pady=(10, 5))

        # Valor principal (ajustado a colores de imagen)
        self.value_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            text= str(MedicionesModel().obtener_medicion(get_planta_id(), "ec")) + " mS/cm",
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

        # Icono para la caja adicional (usando una imagen en lugar de texto)
        self.ph_icon_image = customtkinter.CTkImage(Image.open("icons/1.png"), size=(72, 72))  # Tamaño ajustado
        self.ph_icon_label = customtkinter.CTkLabel(
            self.additional_bordered_box,
            image=self.ph_icon_image,
            text=""
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

        # Icono para la caja central (en vertical) usando una imagen
        self.temp_icon_image = customtkinter.CTkImage(Image.open("icons/3.png"), size=(62, 78))  # Tamaño ajustado
        self.temp_icon_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            image=self.temp_icon_image,
            text=""
        )
        self.temp_icon_label.grid(row=0, column=0, pady=(10, 5))

        # Etiqueta para el valor (27 °C) con tamaño aumentado y en negrita
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

        # Icono para el nivel del agua (usando una imagen en lugar de texto)
        self.water_level_icon_image = customtkinter.CTkImage(Image.open("icons/4.png"), size=(62, 72))  # Reducir ancho
        self.water_level_icon = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            image=self.water_level_icon_image,
            text=""
        )
        self.water_level_icon.grid(row=0, column=0, pady=(10, 5))

        # Etiqueta para el valor (30)
        self.water_level_value = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            text=str(int(nivel_de_agua(get_planta_id()))) + " %",
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
        self.update_mediciones()

    def update_mediciones(self):
        try:
            planta_id = get_planta_id()

            # Conductividad eléctrica
            ec = MedicionesModel().obtener_medicion(planta_id, "ec")
            self.value_label.configure(text=f"{ec} mS/cm")

            # pH
            ph = MedicionesModel().obtener_medicion(planta_id, "ph")
            self.ph_value_label.configure(text=f"{ph} ph")

            # Temperatura
            temp = MedicionesModel().obtener_medicion(planta_id, "temp")
            self.temp_value_label.configure(text=f"{temp} °C")

            # Nivel de agua
            water = nivel_de_agua(get_planta_id())
            self.water_level_value.configure(text=f"{int(water)} %")
        except Exception as e:
            # En caso de error, opcionalmente mostrar en consola o label de error
            print(f"Error actualizando mediciones: {e}")
        finally:
            # Reprograma la siguiente actualización
            self.after(5000, self.update_mediciones)
