import customtkinter

class ConfigView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        label = customtkinter.CTkLabel(self, text="Vista de Configuraci�n", font=("Arial", 20))
        label.pack(pady=20)

        # Bot�n para abrir ventana de correos
        self.email_button = customtkinter.CTkButton(self, text="Agregar correos electr�nicos", command=self.open_email_window)
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

        # Pregunta de seguridad para cambiar contrase�a
        self.security_question_label = customtkinter.CTkLabel(self, text="�Cu�l es tu planeta enano favorito?")
        self.security_question_label.pack(pady=(20, 0))
        self.security_answer_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Respuesta")
        self.security_answer_entry.pack(pady=5)

        # Entrada para contrase�a (deshabilitada por defecto)
        self.password_label = customtkinter.CTkLabel(self, text="Nueva contrase�a:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = customtkinter.CTkEntry(self, width=200, show="*", placeholder_text="Nueva contrase�a")
        self.password_entry.configure(state="disabled")
        self.password_entry.pack(pady=5)

        # Bot�n para verificar respuesta
        self.verify_button = customtkinter.CTkButton(self, text="Verificar respuesta", command=self.verify_security_answer)
        self.verify_button.pack(pady=10)

        # Bot�n para guardar configuraci�n
        save_button = customtkinter.CTkButton(self, text="Guardar configuraci�n", command=self.save_config)
        save_button.pack(pady=30)

        # Lista para almacenar correos
        self.emails = []

    def open_email_window(self):
        # Ventana emergente para ingresar correos
        email_window = customtkinter.CTkToplevel(self)
        email_window.title("Agregar correos electr�nicos")
        email_window.geometry("400x300")

        email_labels = []
        self.email_entries = []

        for i in range(3):
            label = customtkinter.CTkLabel(email_window, text=f"Correo {i+1}:")
            label.pack(pady=(10, 0))
            entry = customtkinter.CTkEntry(email_window, width=300, placeholder_text="ejemplo@correo.com")
            entry.pack(pady=5)
            email_labels.append(label)
            self.email_entries.append(entry)

        def save_emails():
            self.emails = [entry.get() for entry in self.email_entries]
            print("Correos guardados:", self.emails)
            email_window.destroy()

        save_button = customtkinter.CTkButton(email_window, text="Guardar correos", command=save_emails)
        save_button.pack(pady=20)

    def verify_security_answer(self):
        respuesta = self.security_answer_entry.get()
        if respuesta.strip().lower() == "ceres":
            self.password_entry.configure(state="normal")
            customtkinter.CTkLabel(self, text="Respuesta correcta, puedes cambiar la contrase�a.").pack(pady=5)
        else:
            customtkinter.CTkLabel(self, text="Respuesta incorrecta. Intenta de nuevo.", text_color="red").pack(pady=5)

    def save_config(self):
        tiempo_lectura = self.read_time_option.get()
        nueva_contrasena = self.password_entry.get() if self.password_entry.cget("state") == "normal" else None

        print("Tiempo de lectura:", tiempo_lectura)
        print("Correos electr�nicos:", self.emails)
        print("Nueva contrase�a:", nueva_contrasena if nueva_contrasena else "No modificada")
        # Aqu� puedes agregar l�gica adicional para guardar los datos
