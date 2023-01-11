import smtplib
from email.message import EmailMessage 
import os

from dotenv import load_dotenv

load_dotenv()

SENDER = "mx-ena-it@nidec-ga.com"
PASSWORD = "mtxehlzhotoqfeck"

def generate_message(subject, message, receiver, sender=SENDER):
    # Creamos el mensaje
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(message) 
    return msg

def send_mail(sender, password, receiver, msg):
    # Creamos una conexión con el servidor SMTP y enviamos el mensaje
    server = smtplib.SMTP('smtp.embraco.com', '587')
    server.starttls()
    print("Enviando mensaje")
    server.login(sender, password)
    print("Mensaje enviado")
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()