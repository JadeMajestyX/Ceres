import customtkinter
from utils.functions.functions import update_tiempo_lectura, update_email, update_password, get_email

class ConfigView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        label = customtkinter.CTkLabel(self, text="Vista de Configuración", font=("Arial", 20))
        label.pack(pady=20)

        # Botón para abrir ventana de correo
        self.email_button = customtkinter.CTkButton(self, text="Agregar correo electrónico", command=self.open_email_window)
        self.email_button.pack(pady=10)

        # Desplegable para tiempo de lectura
        self.read_time_label = customtkinter.CTkLabel(self, text="Tiempo de lectura del sensor:")
        self.read_time_label.pack(pady=(20, 0))
        self.read_time_option = customtkinter.CTkOptionMenu(
            self, 
            values=["30 minutos", "1 hora", "5 horas"]
        )
        self.read_time_option.set("30 minutos")  # Valor por defecto
        self.read_time_option.pack(pady=5)

        # Pregunta de seguridad para cambiar contraseña
        self.security_question_label = customtkinter.CTkLabel(self, text="¿Cuál es tu planeta enano favorito?")
        self.security_question_label.pack(pady=(20, 0))
        self.security_answer_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Respuesta")
        self.security_answer_entry.pack(pady=5)

        # Entrada para contraseña (deshabilitada por defecto)
        self.password_label = customtkinter.CTkLabel(self, text="Nueva contraseña:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = customtkinter.CTkEntry(self, width=200, show="*", placeholder_text="Nueva contraseña")
        self.password_entry.configure(state="disabled")
        self.password_entry.pack(pady=5)

        # Botón para verificar respuesta
        self.verify_button = customtkinter.CTkButton(self, text="Verificar respuesta", command=self.verify_security_answer)
        self.verify_button.pack(pady=10)

        # Botón para guardar configuración
        save_button = customtkinter.CTkButton(self, text="Guardar configuración", command=self.save_config)
        save_button.pack(pady=30)

        # Variable para almacenar el correo
        self.email = ""

    def open_email_window(self):
        # Ventana emergente para ingresar correo
        email_window = customtkinter.CTkToplevel(self)
        email_window.title("Agregar correo electrónico")
        email_window.geometry("400x200")

        label = customtkinter.CTkLabel(email_window, text="Correo electrónico:")
        label.pack(pady=(20, 0))
        self.email_entry = customtkinter.CTkEntry(email_window, width=300, placeholder_text="ejemplo@correo.com")
        self.email_entry.pack(pady=10)

        def save_email():
            self.email = self.email_entry.get()
            print("Correo guardado:", self.email)
            email_window.destroy()

        save_button = customtkinter.CTkButton(email_window, text="Guardar correo", command=save_email)
        save_button.pack(pady=20)

    def verify_security_answer(self):
        # Verificar la respuesta de seguridad
        correo = get_email()
        if correo:
            self.email = correo
        else:
            self.email = None

        respuesta = self.security_answer_entry.get()
        if respuesta.strip().lower() == self.email.strip().lower():
            self.password_entry.configure(state="normal")
            customtkinter.CTkLabel(self, text="Respuesta correcta, puedes cambiar la contraseña.").pack(pady=5)
        else:
            customtkinter.CTkLabel(self, text="Respuesta incorrecta. Intenta de nuevo.", text_color="red").pack(pady=5)

    def save_config(self):
        tiempo_lectura = self.read_time_option.get()
        nueva_contrasena = self.password_entry.get() if self.password_entry.cget("state") == "normal" else None

        if tiempo_lectura == "30 minutos":
            update_tiempo_lectura(1800)
        elif tiempo_lectura == "1 hora":
            update_tiempo_lectura(3600)
        elif tiempo_lectura == "5 horas":
            update_tiempo_lectura(18000)

        #actualizar email si se ha definido
        if self.email:
            # Aquí puedes agregar la lógica para guardar el correo electrónico
            update_email(self.email)

        #cambiar contraseña si se ha definido
        if nueva_contrasena:
            # Aquí puedes agregar la lógica para cambiar la contraseña
            update_password(nueva_contrasena)
            
            

        print("Tiempo de lectura:", tiempo_lectura)
        print("Correo electrónico:", self.email if self.email else "No definido")
        print("Nueva contraseña:", nueva_contrasena if nueva_contrasena else "No modificada")
        # Aquí puedes agregar lógica adicional para guardar los datos
