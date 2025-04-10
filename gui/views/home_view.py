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

        # Recuadro superior izquierdo

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

        # Add a bordered box inside the bottom bordered box (left side)
        self.inner_bordered_box = customtkinter.CTkFrame(self.bottom_bordered_box, fg_color="#E5F4F4", corner_radius=10)
        self.inner_bordered_box.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Add another bordered box inside the bottom bordered box (right side)
        self.additional_bordered_box = customtkinter.CTkFrame(self.bottom_bordered_box, fg_color="#CFEDED", corner_radius=10)
        self.additional_bordered_box.grid(row=0, column=1, padx=(10, 10), pady=20, sticky="nsew")

        # Add a bordered box inside the bottom bordered box (center)
        self.center_bordered_box = customtkinter.CTkFrame(self.bottom_bordered_box, fg_color="#D6F7F7", corner_radius=10)
        self.center_bordered_box.grid(row=0, column=2, padx=(10, 10), pady=20, sticky="nsew")

        # Add another bordered box inside the bottom bordered box (far right)
        self.far_right_bordered_box = customtkinter.CTkFrame(self.bottom_bordered_box, fg_color="#B8EAEA", corner_radius=10)
        self.far_right_bordered_box.grid(row=0, column=3, padx=(10, 20), pady=20, sticky="nsew")

        # Add labels to each bordered box
        self.inner_label = customtkinter.CTkLabel(self.inner_bordered_box, text="Caja Izquierda", text_color="#114C5F")
        self.inner_label.pack(padx=10, pady=10)

        self.additional_label = customtkinter.CTkLabel(self.additional_bordered_box, text="Nueva Caja", text_color="#114C5F")
        self.additional_label.pack(padx=10, pady=10)

        self.center_label = customtkinter.CTkLabel(self.center_bordered_box, text="Caja Central", text_color="#114C5F")
        self.center_label.pack(padx=10, pady=10)

        self.far_right_label = customtkinter.CTkLabel(self.far_right_bordered_box, text="Caja Derecha", text_color="#114C5F")
        self.far_right_label.pack(padx=10, pady=10)

        ##################################
        ### Finaliza Recuadro inferior ###
        ##################################
