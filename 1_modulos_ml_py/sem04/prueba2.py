# CORREO
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage
import smtplib

emailemisor =  "fduilioomarquispe@gmail.com"
password = "rlot ybep mzur ykdr"
emailreceptor = "floresquispeomar8@gmail.com"

subject = "Hola"

em = EmailMessage()
em["From"] =  emailemisor
em["To"] = emailreceptor
em["Subject"] = subject
em.set_content('Mensaje de prueba')

with open ("Meme.jpg","rb") as f:
    em.add_attachment(
        f.read(),
            filename = "meme.jpg",
            maintype = "image",
            subtype="jpeg"
    )

cliente= smtplib.SMTP('smtp.gmail.com',587)
cliente.starttls()
cliente.login('fduilioomarquispe@gmail.com', 'rlot ybep mzur ykdr')

cliente.send_message(em)