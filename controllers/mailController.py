import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mailController:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "ceresapp14@gmail.com"
        self.password = "ktew vllw fgkp pekp"

    def send_email(self, receiver_email, subject, alerta):
        # Crear mensaje multipart (texto + HTML)
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-ID"] = email.utils.make_msgid()
        msg["Reply-To"] = self.sender_email

        # Texto plano y HTML
        text = f"Alerta: {alerta}. Por favor, verifique el sistema."
        html = f"""
        <html>
        <body>
            <p><strong style="color:red;">Alerta:</strong> <strong>{alerta}</strong>.</p>
            <p>Por favor, verifique el sistema.</p>
        </body>
        </html>
        """

        # Adjuntar ambas partes
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Enviar el correo
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
            print("Correo enviado exitosamente.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
