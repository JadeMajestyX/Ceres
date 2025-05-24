import customtkinter
from PIL import Image  # Import PIL for image handling
from tkinter import messagebox  # Import messagebox for displaying information dialogs
from models.medicionesModel import MedicionesModel
from utils.functions.functions import get_planta_id, nivel_de_agua, tiempo
from models.alertasModel import AlertasModel
import json

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
        self.bordered_box = customtkinter.CTkFrame(self, fg_color="#9CD2D3", corner_radius=20)
        self.bordered_box.grid(row=0, column=0, padx=(40, 20), pady=(40, 20), sticky="nsew")

        # Add a label to display the plant being cultivated
        self.plant_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Cultivo: Tomates",
            font=("Arial", 32, "bold"),
            text_color="#114C5F"
        )
        self.plant_label.pack(padx=30, pady=(20, 15))

        # Add an image label to display the status
        self.status_image_label = customtkinter.CTkLabel(self.bordered_box, text="")
        self.status_image_label.pack(padx=30, pady=(15, 15))

        # Add a label to display the number of days the plant has been growing
        self.days_label = customtkinter.CTkLabel(
            self.bordered_box,
            text="Días de cultivo: " + str(tiempo()),
            font=("Arial", 28, "bold"),
            text_color="#393939"
        )
        self.days_label.pack(padx=30, pady=(15, 20))

        alertas = AlertasModel().obtener_alertas(get_planta_id())

        # Function to update the image based on values
        def update_status_image(values):
            if all(value == "good" for value in values):
                image = customtkinter.CTkImage(Image.open("icons/Muy bien.png"), size=(160, 160))
                self.status_image_label.configure(image=image)
            elif sum(1 for value in values if value == "bad") <= 2:
                image = customtkinter.CTkImage(Image.open("icons/maso menos.png"), size=(160, 160))
                self.status_image_label.configure(image=image)
            else:
                image = customtkinter.CTkImage(Image.open("icons/mal.png"), size=(160, 160))
                self.status_image_label.configure(image=image)

        # Replace these with actual logic to determine the status of each value
        example_values = ["good", "bad", "good", "bad"]
        update_status_image(example_values)

        #####################################
        #### Recuadro superior derecho ######
        #####################################

        # Create a top-right bordered box for notifications
        self.notifications_box = customtkinter.CTkFrame(
            self, fg_color="#9CD2D3", corner_radius=20
        )
        self.notifications_box.grid(
            row=0, column=1, padx=(20, 40), pady=(40, 20), sticky="nsew"
        )

        # Configure grid weights for rescalability
        self.notifications_box.grid_rowconfigure(0, weight=1)
        self.notifications_box.grid_columnconfigure(0, weight=1)

        # Add a scrollable frame inside the notifications box
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.notifications_box,
            fg_color="#9CD2D3",
            corner_radius=20,
            width=500
        )
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Title label
        self.notifications_label = customtkinter.CTkLabel(
            self.scrollable_frame,
            text="Notificaciones",
            text_color="#114C5F",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        self.notifications_label.grid(row=0, column=0, padx=20, pady=(10, 30), sticky="ew")

        # Lista de widgets de notificación para evitar parpadeo
        self.notification_widgets = []  # [(frame, icon_label, content_label)]

        def add_notification_widget(text, severity="info"):
            # Crea el frame y devuelve sus componentes
            frame = customtkinter.CTkFrame(
            self.scrollable_frame,
            fg_color="#E0F7FA",
            corner_radius=20
            )
            frame.grid_columnconfigure((0, 1), weight=1)
            icon_label = customtkinter.CTkLabel(
            frame,
            text="ℹ️" if severity == "info" else ("⚠️" if severity == "warning" else "❌"),
            font=("Arial", 24, "bold"),
            text_color=("#114C5F" if severity == "info" else ("#FFA500" if severity == "warning" else "#FF0000"))
            )
            icon_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
            content_label = customtkinter.CTkLabel(
            frame,
            text=text,
            text_color="#114C5F",
            font=("Arial", 20),
            anchor="w"
            )
            content_label.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
            return frame, icon_label, content_label

        def update_alerts():
            nuevas = AlertasModel().obtener_alertas(get_planta_id())
            # Actualizar o crear widgets existentes
            for idx, alerta in enumerate(nuevas):
                texto = alerta[3]
                if texto in self.errors:
                    sev = "error"
                elif texto in self.warnings:
                    sev = "warning"
                else:
                    sev = "info"
                if idx < len(self.notification_widgets):
                    frame, icon_label, content_label = self.notification_widgets[idx]
                    # Solo reposicionar grid si es la primera vez
                    if not frame.winfo_ismapped():
                        frame.grid(row=idx+1, column=0, padx=10, pady=10, sticky="ew")
                    # Actualizar icono y texto
                    icon_label.configure(text=icon_label.cget("text") if icon_label.cget("text") == ("ℹ️" if sev=="info" else ("⚠️" if sev=="warning" else "❌")) else ("ℹ️" if sev=="info" else ("⚠️" if sev=="warning" else "❌")), text_color=("#114C5F" if sev=="info" else ("#FFA500" if sev=="warning" else "#FF0000")))
                    content_label.configure(text=texto)
                else:
                    # Crear nuevo widget
                    frame, icon_label, content_label = add_notification_widget(texto, sev)
                    frame.grid(row=idx+1, column=0, padx=10, pady=10, sticky="ew")
                    self.notification_widgets.append((frame, icon_label, content_label))
            # Destruir widgets sobrantes
            for extra in range(len(nuevas), len(self.notification_widgets)):
                frame, _, _ = self.notification_widgets[extra]
                frame.grid_forget()
            # Mantener solo los necesarios
            self.notification_widgets = self.notification_widgets[:len(nuevas)]
            # Programar siguiente actualización
            self.after(5000, update_alerts)

        # Iniciar actualizaciones
        update_alerts()

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
            fg_color="#A6F0FF",  # Fondo blanco (como en la imagen)
            corner_radius=10,
            border_width=1,
            border_color="#A6F0FF"  # Borde gris claro (más discreto que en tu versión original)
        )
        self.inner_bordered_box.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Configuración de grid (igual que antes)
        self.inner_bordered_box.grid_rowconfigure(0, weight=1)
        self.inner_bordered_box.grid_rowconfigure(1, weight=1)
        self.inner_bordered_box.grid_rowconfigure(2, weight=1)
        self.inner_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono (usando una imagen en lugar de texto)
        self.icon_image = customtkinter.CTkImage(Image.open("assets/images/CE.png"), size=(72, 72))  # Tamaño aumentado
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
            text_color="#393939"  # Mismo color que el icono
        )
        self.value_label.grid(row=1, column=0, pady=(5, 5))

        # Título (ajustado a colores de imagen)
        self.title_label = customtkinter.CTkLabel(
            self.inner_bordered_box,
            text="Conductividad eléctrica",
            font=("Arial", 18, "bold"),
            text_color="#393939"  # Mismo color que los demás textos
        )
        self.title_label.grid(row=2, column=0, pady=(5, 10))

        # Botón de información redondo y pequeño en la esquina superior derecha
        def show_ec_info():
            messagebox.showinfo(
            title="Información de Conductividad Eléctrica",
            message=(
            "La conductividad eléctrica mide la capacidad del agua para conducir electricidad, "
            "lo cual está relacionado con la cantidad de sales disueltas.\n\n"
            "Rangos:\n"
            "- Crítico: Menor a 0.2 mS/cm o mayor a 3.0 mS/cm.\n"
            "- Estable: Entre 0.2 mS/cm y 0.5 mS/cm o entre 2.5 mS/cm y 3.0 mS/cm.\n"
            "- Óptimo: Entre 0.5 mS/cm y 2.5 mS/cm.\n\n"
            "La conductividad adecuada es esencial para el crecimiento saludable de las plantas."
            )
            )

        self.ec_info_button = customtkinter.CTkButton(
            self.inner_bordered_box,
            text="i",
            command=show_ec_info,
            fg_color="#4A90E2",  # Color azul claro para destacar
            hover_color="#357ABD",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.ec_info_button.place(relx=0.95, rely=0.05, anchor="ne")  # Posicionarlo en la esquina superior derecha

        # Mostrar alertas relacionadas con la conductividad eléctrica
        def show_ec_alerts():
            alertas = AlertasModel().obtener_alertas(get_planta_id())
            ec_alertas = [alerta[3] for alerta in alertas if "conductividad" in alerta[3].lower()]
            if ec_alertas:
                messagebox.showwarning(
                    title="Alertas de Conductividad Eléctrica",
                    message="\n".join(ec_alertas)
                )
            else:
                messagebox.showinfo(
                    title="Sin Alertas",
                    message="No hay alertas relacionadas con la conductividad eléctrica."
                )

        self.ec_alerts_button = customtkinter.CTkButton(
            self.inner_bordered_box,
            text="⚠️",
            command=show_ec_alerts,
            fg_color="#FFA500",  # Color naranja para alertas
            hover_color="#FF8C00",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.ec_alerts_button.place(relx=0.05, rely=0.05, anchor="nw")  # Posicionarlo en la esquina superior izquierda

        ################################
        ### Finzaliza Caja Numero 1 ####
        ################################

        ######################################
        ######   Inicia Caja Numero 2  #######
        ######################################

        self.additional_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box, 
            fg_color="#B2CDFF",  # Color de fondo ligeramente diferente al primero
            corner_radius=10,
            border_width=1,
            border_color="#B2CDFF"  # Mismo color de borde que el primero
        )
        self.additional_bordered_box.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.additional_bordered_box.grid_rowconfigure((0, 1, 2), weight=1)
        self.additional_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para la caja adicional (usando una imagen en lugar de texto)
        self.ph_icon_image = customtkinter.CTkImage(Image.open("assets/images/ph.png"), size=(72, 72))  # Tamaño ajustado
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
            text_color="#393939"  # Mismo color de texto que el primero
        )
        self.ph_value_label.grid(row=1, column=0, pady=(5, 5))

        # Etiqueta para la descripción
        self.ph_title_label = customtkinter.CTkLabel(
            self.additional_bordered_box,
            text="Acidez o alcalinidad",
            font=("Arial", 18, "bold"),  # Tamaño más grande y en negrita
            text_color="#393939"
        )
        self.ph_title_label.grid(row=2, column=0, pady=(5, 10))

        # Botón de información redondo y pequeño en la esquina superior derecha
        def show_ph_info():
            messagebox.showinfo(
            title="Información del pH",
            message=(
            "El pH mide la acidez o alcalinidad del agua.\n\n"
            "Rangos:\n"
            "- Crítico: Muy ácido (pH menor a 4) o muy alcalino (pH mayor a 10).\n"
            "- Estable: Moderadamente ácido (pH entre 4 y 6) o moderadamente alcalino (pH entre 8 y 10).\n"
            "- Óptimo: Neutral o ligeramente ácido/alcalino (pH entre 6 y 8).\n\n"
            "El pH mínimo es 0 y el máximo es 14."
            )
            )

        self.ph_info_button = customtkinter.CTkButton(
            self.additional_bordered_box,
            text="i",
            command=show_ph_info,
            fg_color="#4A90E2",  # Color azul claro para destacar
            hover_color="#357ABD",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15 # Hacerlo completamente circular
        )
        self.ph_info_button.place(relx=0.95, rely=0.05, anchor="ne")  # Posicionarlo en la esquina superior derecha

        # Botón para mostrar alertas relacionadas con el pH
        def show_ph_alerts():
            alertas = AlertasModel().obtener_alertas(get_planta_id())
            ph_alertas = [alerta[3] for alerta in alertas if "ph" in alerta[3].lower()]
            if ph_alertas:
                messagebox.showwarning(
                    title="Alertas de pH",
                    message="\n".join(ph_alertas)
                )
            else:
                messagebox.showinfo(
                    title="Sin Alertas",
                    message="No hay alertas relacionadas con el pH."
                )

        self.ph_alerts_button = customtkinter.CTkButton(
            self.additional_bordered_box,
            text="⚠️",
            command=show_ph_alerts,
            fg_color="#FFA500",  # Color naranja para alertas
            hover_color="#FF8C00",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.ph_alerts_button.place(relx=0.05, rely=0.05, anchor="nw")  # Posicionarlo en la esquina superior izquierda

        #######################################
        ###### Finzaliza Caja Numero 2 ########
        #######################################

        ####################################
        ####### Inicia Caja Numero 3########
        ####################################

        self.center_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box,
            fg_color="#87E2FF",  # Color de fondo intermedio entre los dos anteriores
            corner_radius=10,
            border_width=1,
            border_color="#87E2FF"  # Mismo color de borde consistente
        )
        self.center_bordered_box.grid(row=0, column=2, padx=(10, 10), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.center_bordered_box.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.center_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para la caja central (en vertical) usando una imagen
        self.temp_icon_image = customtkinter.CTkImage(Image.open("assets/images/Temp.png"), size=(70, 78))  # Tamaño ajustado
        self.temp_icon_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            image=self.temp_icon_image,
            text=""
        )
        self.temp_icon_label.grid(row=0, column=0, pady=(10, 5))

        # Etiqueta para el valor (27 °C) con tamaño aumentado y en negrita
        self.temp_value_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text= str(MedicionesModel().obtener_medicion(get_planta_id(), "temp_planta")) + " °C",
            font=("Arial", 28, "bold"),  # Tamaño más grande y en negrita
            text_color="#393939"  # Mismo esquema de colores
        )
        self.temp_value_label.grid(row=1, column=0, pady=(5, 5))

        # Etiqueta para la descripción
        self.temp_title_label = customtkinter.CTkLabel(
            self.center_bordered_box,
            text="Temperatura de la planta",
            font=("Arial", 18, "bold"),  # Tamaño más grande y en negrita
            text_color="#393939"
        )
        self.temp_title_label.grid(row=2, column=0, pady=(5, 10))

        # Botón de información redondo y pequeño en la esquina superior derecha
        def show_temp_info():
            messagebox.showinfo(
            title="Información de la Temperatura",
            message="La temperatura de la planta es crucial para su desarrollo.\n"
            "Mínimo recomendado: 18°C\nMáximo recomendado: 30°C"
            )

        self.temp_info_button = customtkinter.CTkButton(
            self.center_bordered_box,
            text="i",
            command=show_temp_info,
            fg_color="#4A90E2",  # Color azul claro para destacar
            hover_color="#357ABD",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.temp_info_button.place(relx=0.95, rely=0.05, anchor="ne")  # Posicionarlo en la esquina superior derecha

        # Botón para mostrar alertas relacionadas con la temperatura
        def show_temp_alerts():
            alertas = AlertasModel().obtener_alertas(get_planta_id())
            temp_alertas = [alerta[3] for alerta in alertas if "temperatura" in alerta[3].lower()]
            if temp_alertas:
                messagebox.showwarning(
                    title="Alertas de Temperatura",
                    message="\n".join(temp_alertas)
                )
            else:
                messagebox.showinfo(
                    title="Sin Alertas",
                    message="No hay alertas relacionadas con la temperatura."
                )

        self.temp_alerts_button = customtkinter.CTkButton(
            self.center_bordered_box,
            text="⚠️",
            command=show_temp_alerts,
            fg_color="#FFA500",  # Color naranja para alertas
            hover_color="#FF8C00",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.temp_alerts_button.place(relx=0.05, rely=0.05, anchor="nw")  # Posicionarlo en la esquina superior izquierda

        #######################################
        ####### Finaliza Caja Numero 3 ########
        #######################################

        ########################################
        #######  Inicia Caja Numero 4  #########
        ########################################

        self.far_right_bordered_box = customtkinter.CTkFrame(
            self.bottom_bordered_box,
            fg_color="#FFF8E9",  # Color de fondo ligeramente más oscuro para diferenciación visual
            corner_radius=10,
            border_width=1,
            border_color="#FFF8E9"  # Mantiene consistencia con los otros cuadros
        )
        self.far_right_bordered_box.grid(row=0, column=3, padx=(10, 20), pady=20, sticky="nsew")

        # Configurar el sistema de pesos para centrar el contenido
        self.far_right_bordered_box.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.far_right_bordered_box.grid_columnconfigure(0, weight=1)

        # Icono para el nivel del agua (usando una imagen en lugar de texto)
        self.water_level_icon_image = customtkinter.CTkImage(Image.open("assets/images/LW.png"), size=(68, 72))  # Reducir ancho
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
            text_color="#393939"  # Mismo esquema de colores
        )
        self.water_level_value.grid(row=1, column=0, pady=(5, 5))

        # Etiqueta para la descripción
        self.water_level_title = customtkinter.CTkLabel(
            self.far_right_bordered_box,
            text="Nivel del agua",
            font=("Arial", 18, "bold"),  # Negrita
            text_color="#393939"
        )
        self.water_level_title.grid(row=2, column=0, pady=(5, 10))

        # Botón de información redondo y pequeño en la esquina superior derecha
        def show_water_info():
            from tkinter import messagebox
            messagebox.showinfo(
            title="Información del Nivel de Agua",
            message="El nivel de agua indica la cantidad de agua disponible en el sistema.\n"
            "Mínimo recomendado: 20%\nMáximo recomendado: 100%"
            )

        self.info_button = customtkinter.CTkButton(
            self.far_right_bordered_box,
            text="i",
            command=show_water_info,
            fg_color="#4A90E2",  # Color azul claro para destacar
            hover_color="#357ABD",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.info_button.place(relx=0.95, rely=0.05, anchor="ne")  # Posicionarlo en la esquina superior derecha

        # Botón para mostrar alertas relacionadas con el nivel de agua
        def show_water_alerts():
            alertas = AlertasModel().obtener_alertas(get_planta_id())
            water_alertas = [alerta[3] for alerta in alertas if "agua" in alerta[3].lower()]
            if water_alertas:
                messagebox.showwarning(
                    title="Alertas de Nivel de Agua",
                    message="\n".join(water_alertas)
                )
            else:
                messagebox.showinfo(
                    title="Sin Alertas",
                    message="No hay alertas relacionadas con el nivel de agua."
                )

        self.water_alerts_button = customtkinter.CTkButton(
            self.far_right_bordered_box,
            text="⚠️",
            command=show_water_alerts,
            fg_color="#FFA500",  # Color naranja para alertas
            hover_color="#FF8C00",  # Color más oscuro al pasar el mouse
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            width=30,  # Tamaño pequeño
            height=30,  # Tamaño pequeño
            corner_radius=15  # Hacerlo completamente circular
        )
        self.water_alerts_button.place(relx=0.05, rely=0.05, anchor="nw")  # Posicionarlo en la esquina superior izquierda

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
            print(water)
            self.water_level_value.configure(text=f"{int(water)} %")
        except Exception as e:
            # En caso de error, opcionalmente mostrar en consola o label de error
            print(f"Error actualizando mediciones: {e}")
        finally:
            # Reprograma la siguiente actualización
            self.after(5000, self.update_mediciones)