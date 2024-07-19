import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

email = input("Enter your email: ")
password = input("Enter your password: ")
server.login(email, password)

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = ""
msg['Subject'] = "Test"
body = "Hello"
msg.attach(MIMEText(body, 'plain'))

filename = "../data/pillars_of_creation.jpg"
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(p)

text = msg.as_string()
server.sendmail(email, "", text)
