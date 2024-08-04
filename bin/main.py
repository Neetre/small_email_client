'''
This program will auto respond to a certain type of emails

Neetre 2024
'''

import os
from dotenv import load_dotenv
load_dotenv()
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from read_email import read_email
from send_email import send_email

from filters import EMAILS


EMAIL_ACCOUNT = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
GROQ_API_KEY=os.environ["GROQ_API_KEY"]


def auto_response(body):
    message = f"Respond to this email's body: {body}"
    chat = ChatGroq(temperature=1, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")

    system = "Respond to the email as if you were a person writing a response."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    response = chain.invoke({"text": message})
    text_response = response.content
    
    return text_response


def clean_response(text_response, signature="Name"):
    try:
        squared_brackets = text_response.index("[")
        return text_response[:squared_brackets] + signature
    except ValueError:
        return text_response + "\n" + signature


def show_emails(emails: list):
    for email in emails:
        yield email


def show_email(email_generator):
    while True:
        try:
            email = next(email_generator)
            print("\nID:", email["ID"])
            print("From:", email["From"])
            print("Subject:", email["Subject"])
            print("Date:", email["Date"])
            print("Body:", email["Body"])
            print("Message-ID:", email["Message-ID"])

            next_email = input("\nDo you want to see the next email? (y/n): ")
            if next_email.lower() == 'n':
                break
        except StopIteration:
            print("No more emails!")
            break


def send(email):
    body = email["Body"]
    to_email = email["From"]
    ok = False
    while not ok:
        text_response = auto_response(body)
        print("Response:\n", text_response)
        text_response = clean_response(text_response)
        print("Cleaned Response:\n", text_response)
        
        is_response_correct = input(f"Is this the correct response? (y/n):")
        if is_response_correct.lower() == 'n':
            print("Regenerating response...")
            continue
        ok = True
        subject = email["Subject"]
        reference = (email["References"] or "") + " " + email["Message-ID"]
        message_id = email["Message-ID"]
        
        skip = input("Do you want to skip sending the email? (y/n): ")
        if skip.lower() == 'y':
            print("Email not sent!")
        
        send_email(to_email, subject, reference, message_id, text_response)  # to_email, subject, reference, message_id, body, filepath: str = None
        print("Email sent!")


def main():
    for email in EMAILS if isinstance(EMAILS, list) else [input("Enter the email to respond to: ").strip()]:
        if email == "":
            print("No email provided!")
            email = None

        print(f"Email: {email}")
        mailbox = 'inbox'
        filter = 'UNSEEN'
        email_filter = "FROM '{}'".format(email)
        emails = read_email(mailbox, filter, email_filter)
        print(len(emails), "emails found!")
        if len(emails) == 0:
            print("No emails found!")
            return

        # email_generator = show_emails(emails)
        # show_email(email_generator)

        # email_id = input("Enter the email id to respond to: ")
        # email = next((e for e in emails if e["ID"] == email_id.encode()), None)
        email = emails[0]
        if email is None:
            print("Email not found!")
            return
        
        
        send(email)


if __name__ == "__main__":
    main()