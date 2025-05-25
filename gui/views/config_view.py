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
        self.security_question_label = customtkinter.CTkLabel(self, text="Coreo electrónico (pregunta de seguridad):")
        self.security_question_label.pack(pady=(20, 0))
        self.security_answer_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Respuesta")
        self.security_answer_entry.pack(pady=5)

        # Entrada para contraseña (deshabilitada por defecto)
        self.password_label = customtkinter.CTkLabel(self, text="Nueva contraseña:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = customtkinter.CTkEntry(self, width=200, show="*", placeholder_text="Nueva contraseña")
        self.password_entry.configure(state="disabled")
        self.password_entry.pack(pady=5)

        # Mensaje de verificación
        self.verification_message = customtkinter.CTkLabel(self, text="")
        self.verification_message.pack(pady=5)

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
        respuesta = self.security_answer_entry.get().strip().lower()

        email = get_email().strip().lower()

        if respuesta == email:
            self.password_entry.configure(state="normal")
            self.verification_message.configure(text="Respuesta correcta, puedes cambiar la contraseña.", text_color="green")
        else:
            self.password_entry.configure(state="disabled")
            self.verification_message.configure(text="Respuesta incorrecta. Intenta de nuevo.", text_color="red")

    def save_config(self):
        tiempo_lectura = self.read_time_option.get()
        nueva_contrasena = self.password_entry.get() if self.password_entry.cget("state") == "normal" else None

        if tiempo_lectura == "30 minutos":
            update_tiempo_lectura(1800)
        elif tiempo_lectura == "1 hora":
            update_tiempo_lectura(3600)
        elif tiempo_lectura == "5 horas":
            update_tiempo_lectura(18000)

        # Guardar correo si se ha definido
        if self.email:
            update_email(self.email)

        # Cambiar contraseña si es válida
        if nueva_contrasena:
            update_password(nueva_contrasena)

        print("Tiempo de lectura:", tiempo_lectura)
        print("Correo electrónico:", self.email if self.email else "No definido")
        print("Nueva contraseña:", nueva_contrasena if nueva_contrasena else "No modificada")
