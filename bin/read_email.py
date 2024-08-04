import imaplib
import email
from email.header import decode_header
import os

# Configuration
IMAP_SERVER = 'imap.gmail.com'

EMAIL_ACCOUNT = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

def smtp_server(email):
    domain = email.split("@")[1]
    domain = "smtp." + domain
    return domain


def read_email(mailbox='inbox', filter='UNSEEN', email_filter=None) -> list:
    emails = []
    server = smtp_server(EMAIL_ACCOUNT)
    mail = imaplib.IMAP4_SSL(server)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    mail.select(mailbox)
    search_filter = filter if email_filter is None else email_filter
    status, email_ids = mail.search(None, search_filter)
    email_ids = email_ids[0].split()
    
    for e_id in email_ids:
        _, data = mail.fetch(e_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        # print(f"Message Number: {e_id}")
        # print(f"From: {email_message.get('From')}")
        # print(f"To: {email_message.get('To')}")
        # print(f"BCC: {email_message.get('BCC')}")  # BCC is not always present, it is a list of emails separated by commas
        # print(f"Date: {email_message.get('Date')}")
        # print(f"Subject: {email_message.get('Subject')}")
        
        msg = {
            "ID": e_id,
            "From": email_message.get("From"),
            "To": email_message.get("To"),
            "BCC": email_message.get("BCC"),
            "Date": email_message.get("Date"),
            "Subject": email_message.get("Subject"),
            "References": email_message.get("References"),
            "Message-ID" : email_message.get("Message-ID"),
            "Body": ""
        }

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    msg["Body"] = body
        else:
            content_type = email_message.get_content_type()
            body = email_message.get_payload(decode=True).decode()
            msg["Body"] = body
        emails.append(msg)

    mail.close()
    mail.logout()
    print(f"{len(emails)} emails found!")
    return emails

    
def main():
    read_email()
    

if __name__ == '__main__':
    main()
