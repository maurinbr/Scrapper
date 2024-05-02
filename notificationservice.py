import smtplib
from email.message import EmailMessage

def send_email(subject, body, sender_email, receiver_email, password):
    # Configuration du serveur SMTP Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Port SMTP TLS

    # Création du message
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message.set_content(body)

    # Connexion au serveur SMTP Gmail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Activer le chiffrement TLS
        server.login(sender_email, password)
        server.send_message(message)

    print('E-mail envoyé avec succès !')
# Exemple d'utilisation de la fonction send_email pour envoyer un e-mail via Gmail
send_email("Test", "Ceci est un e-mail de test.", "asphalteconvoyage@gmail.com", "bruno.maurin.mtp@gmail.com", "Oligo2$$")
