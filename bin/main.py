'''
This program will auto respond to a certain type of emails

Neetre 2024
'''

import os
import getpass

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from read_email import read_email
from send_email import send_email

if "EMAIL" not in os.environ:
    os.environ["EMAIL"] = getpass.getpass('Enter your email ---> ')
EMAIL_ACCOUNT = os.environ["EMAIL"]

if "PASSWORD" not in os.environ:
    os.environ["PASSWORD"] = getpass.getpass('Enter your email password ---> ')
PASSWORD = os.environ["PASSWORD"]

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Provide your Groq API Key ---> ")
GROQ_API_KEY=os.environ["GROQ_API_KEY"]


def auto_response(message):
    chat = ChatGroq(temperature=1, groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768")

    system = "You are a helpful assistant."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    response = chain.invoke({"text": message})
    text_response = response.content
    
    return text_response


def elab():
    pass

def main():
    respond_to = read_email()
    for email in respond_to:
        message = elab(email)
        text_response = auto_response(message)
        send_email(text_response)