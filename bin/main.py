'''
This program will auto respond to a certain type of emails

Neetre 2024
'''

import os
import getpass
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from read_email import read_email
from send_email import send_email


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


def show_emails(emails: list):
    for email in emails:
        yield email


def main():
    mailbox = 'inbox'
    filter = 'UNSEEN'
    email_filter = "FROM ''"
    emails = read_email(mailbox, filter, email_filter)
    print(len(emails), "emails found!")
    if len(emails) == 0:
        print("No emails found!")
        return

    email_generator = show_emails(emails)
    while True:
        try:
            email = next(email_generator)
            print("\nID:", email["ID"])
            print("From:", email["From"])
            print("Subject:", email["Subject"])
            print("Date:", email["Date"])
            print("Body:", email["Body"])

            next_email = input("\nDo you want to see the next email? (y/n): ")
            if next_email.lower() == 'n':
                break
        except StopIteration:
            print("No more emails!")
            break

    email_id = input("Enter the email id to respond to: ")
    email = next((e for e in emails if e["ID"] == email_id.encode()), None)
    if email is None:
        print("Email not found!")
        return
    body = email["Body"]
    to_email = email["From"]

    text_response = auto_response(body)
    print("Response:", text_response)
    # send_email(to_email, text_response)
    print("Email sent!")


if __name__ == "__main__":
    main()