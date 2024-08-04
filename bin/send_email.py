import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl


EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
SMTP_PORT = 465  # Use 465 for SSL, 587 for TLS


def smtp_server(email):
    domain = email.split("@")[1]
    domain = "smtp." + domain
    return domain


def send_email(to_email, subject, reference, message_id, body, filepath: str = None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Re: " + subject
    msg['In-Reply-To'] = reference
    msg['Message-ID'] = message_id

    msg.attach(MIMEText(body, 'plain'))

    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        elif not os.path.isfile(filepath):
            raise ValueError(f"Path is not a file: {filepath}")
        elif filepath is not None:
            filepath = filepath
            filename = os.path.basename(filepath)
            attachment = open(filepath, 'rb')

            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())

            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)
    except Exception as e:
        print(f"Exception cought while reading filepath: {e}")

    context = ssl.create_default_context()
    SMTP_SERVER = smtp_server(EMAIL)
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())


def main():
    to_email = input("Enter the email of the recipient: ").strip()
    send_email(to_email)
    

if __name__ == "__main__":
    main()
