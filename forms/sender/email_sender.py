import smtplib
from email.message import EmailMessage 
import os

class EmailSender:
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password
        
    def send_mail(self, receiver, subject, message, image_data=None):
        msg = EmailMessage()
        msg['From'] = self.sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.set_content(message) 

        # Creamos una conexión con el servidor SMTP y enviamos el mensaje
        server = smtplib.SMTP('smtp.embraco.com', '587')
        server.starttls()
        print("Enviando mensaje")
        server.login(self.sender, self.password)
        print("Mensaje enviado")
        server.sendmail(self.sender, receiver, msg.as_string())
        server.quit()

