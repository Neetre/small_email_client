import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl

import os
import getpass

EMAIL = os.environ.get('EMAIL') or getpass.getpass('Enter your email: ')
PASSWORD = os.environ.get('PASSWORD') or getpass.getpass('Enter your email password: ')

def send_email(to_email, filepath = None):
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = "cosinize@gmail.com"
    msg['Subject'] = "Test"
    body = "Hello"
    msg.attach(MIMEText(body, 'plain'))

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    elif not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")
    elif filepath is not None:
        filepath = "../data/pillars_of_creation.jpg"
        filename = os.path.basename(filepath)
        attachment = open(filepath, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(p)

    text = msg.as_string()
    server.sendmail(EMAIL, to_email, text)


def main():
    to_email = input("Enter the email of the recipient: ").strip()
    send_email(to_email)