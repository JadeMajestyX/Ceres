import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "ceresapp14@gmail.com"
receiver_email = "carranzaavelinodianakarina@gmail.com"
password = "ktew vllw fgkp pekp"

# Crear el mensaje
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Asunto del correo"

# Cuerpo del mensaje
body = "Este es el cuerpo del correo."
msg.attach(MIMEText(body, "plain"))

# Enviar el correo
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Cifrado
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
