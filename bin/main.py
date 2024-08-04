'''
This program will auto respond to a certain type of emails

Neetre 2024
'''

import os
import getpass
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from read_email import read_email
from send_email import send_email

load_dotenv()
EMAIL_ACCOUNT = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
GROQ_API_KEY=os.environ["GROQ_API_KEY"]


def auto_response(message):
    chat = ChatGroq(temperature=1, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")

    system = "You respond to the email"
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    response = chain.invoke({"text": message})
    text_response = response.content
    
    return text_response


def elab():
    pass

def main():
    mailbox = 'inbox'
    filter = 'UNSEEN'
    respond_to = read_email()
    for email in respond_to:
        to_email, message = elab(email)
        text_response = auto_response(message)
        send_email(text_response)


if __name__ == "__main__":
    main()