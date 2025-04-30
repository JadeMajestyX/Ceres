from controllers.mailController import mailController
import json
from utils.functions.functions import get_email

emails = get_email()

# Asigna a variables
email1 = emails['email1']
email2 = emails['email2']
email3 = emails['email3']

alerta = "Se ha detectado un alto nivel de botsito"
subject = "Alerta"

mailController = mailController()
mailController.send_email(email2, subject, alerta)