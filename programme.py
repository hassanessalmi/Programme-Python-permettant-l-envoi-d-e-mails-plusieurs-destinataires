import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Définir les variables d'environnement directement dans le script (à des fins de démonstration seulement)
os.environ['SMTP_USERNAME'] = 'simhassan06@gmail.com'
os.environ['SMTP_PASSWORD'] = ''

def envoyer_email(destinataires, objet, message, piece_jointe_path=None):
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    if not smtp_username or not smtp_password:
        print("Veuillez définir les variables d'environnement SMTP_USERNAME et SMTP_PASSWORD.")
        return

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    msg['Subject'] = objet
    msg['From'] = smtp_username
    msg['Bcc'] = ', '.join(destinataires[1:])  # Ajout de la liste des destinataires sans le premier (l'expéditeur)

    if piece_jointe_path:
        # Attacher le CV
        cv_attachment = open(piece_jointe_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(cv_attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(piece_jointe_path)}"')
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        for destinataire in destinataires:
            msg.replace_header('Bcc', destinataire)
            server.sendmail(smtp_username, destinataire, msg.as_string())

        print("E-mails envoyés avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

    finally:
        if 'server' in locals():
            server.quit()

# Liste des destinataires
destinataires = ['younesessaddiki99@gmail.com', 'essalmi.hassan96@gmail.com']

# Chemin vers votre CV
cv_path = 'Hassan-Essalmi.pdf'

# Envoyer l'e-mail avec copie cachée individuelle pour chaque destinataire
envoyer_email(destinataires, 'demande de stage PFE2024', 'Bonjour,\n\nJ\'espère que vous allez bien. Je me permets de vous contacter aujourd\'hui afin de manifester mon vif intérêt pour un stage de PFE dans le domaine de l\'ingénierie informatique au sein de votre entreprise.\n\nJe suis actuellement étudiant en ingénierie informatique à l\'Institut supérieur d\'ingénierie et des affaires et je suis passionné par les nouvelles technologies, le développement logiciel et les systèmes d\'information. Ma formation m\'a permis d\'acquérir une solide base de connaissances dans des domaines tels que la programmation, les bases de données, les réseaux et la sécurité informatique.\n\nJe suis convaincu que rejoindre votre entreprise en tant que stagiaire me permettrait d\'appliquer mes connaissances dans un environnement professionnel stimulant. Je suis désireux de travailler sur des projets concrets et de contribuer à l\'évolution des solutions technologiques de votre entreprise.\n\nCordialement,\n\nESSALMI hassan', cv_path)
