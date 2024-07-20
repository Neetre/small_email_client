import imaplib
import email
from email.header import decode_header
import os
import getpass

# Configuration
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ.get('EMAIL') or getpass.getpass('Enter your email: ')
PASSWORD = os.environ.get('PASSWORD') or getpass.getpass('Enter your email password: ')


def read_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    # Select the mailbox you want to check (INBOX, for example)
    mail.select('inbox')
    # Search for specific mails by criteria
    status, email_ids = mail.search(None, 'UNSEEN')  # Use 'UNSEEN' for unread emails, 'ALL' for all emails
    # Convert the result to a list of email IDs
    email_ids = email_ids[0].split()

    for e_id in email_ids:
        # Fetch the email by ID (RFC822 protocol for full email)
        status, data = mail.fetch(e_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject = decode_header(email_message['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        from_ = email_message['From']

        print(f"From: {from_}\nSubject: {subject}\n")

        # If the email message is multipart
        if email_message.is_multipart():
            for part in email_message.walk():
                # Extract content type of the email
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Get the email body
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    print(body)
        else:
            # Extract content type of the email
            content_type = email_message.get_content_type()
            # Get the email body
            body = email_message.get_payload(decode=True).decode()
            print(body)

    mail.close()
    mail.logout()
    

def read_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    mail.select('inbox')
    status, email_ids = mail.search(None, 'UNSEEN')
    email_ids = email_ids[0].split()
    
    for e_id in email_ids:
        _, data = mail.fetch(e_id, "(RFC822)")
        email_message = email.message_from_bytes(data[0][1])
        
        print(f"Message Number: {e_id}")
        print(f"From: {email_message.get('From')}")
        print(f"To: {email_message.get('To')}")
        print(f"BCC: {email_message.get('BCC')}")
        print(f"Date: {email_message.get('Date')}")
        print(f"Subject: {email_message.get('Subject')}")

        print("Content: ")
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    print(body)
        else:
            content_type = email_message.get_content_type()
            body = email_message.get_payload(decode=True).decode()
            print(body)
            
    mail.close()
    mail.logout()

    
def main():
    read_email()
    

if __name__ == '__main__':
    main()