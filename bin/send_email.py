import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl


EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


def smtp_server(email):
    domain = email.split("@")[1]
    domain = "smtp." + domain
    return domain


def send_emails(to_email, subject, body, filepath: str = None):
    server = smtp_server(EMAIL)
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(server, 587, context=context)
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = to_email
    msg['To'] = EMAIL
    msg['Subject'] = subject
    msg.add_header('reply-to', to_email)
    body = body
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

    text = msg.as_string()
    server.sendmail(EMAIL, to_email, text)
    

def send_email():
    pass


def main():
    to_email = input("Enter the email of the recipient: ").strip()
    send_emails(to_email)
    

if __name__ == "__main__":
    main()
