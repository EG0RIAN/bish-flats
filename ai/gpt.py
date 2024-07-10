"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()

SBER_TOKEN = os.getenv("SBER_TOKEN")

chat = GigaChat(credentials=SBER_TOKEN, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный риелтор, который описывыет найденную квартиру"
    )
]


def use_ai(context):
    messages.append(HumanMessage(content=context))
    res = chat(messages)
    return res.content
