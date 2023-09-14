# This code is the is the chatbot OpenAI gpt-3.5-turbo model that uses embeddings it uses langchain as workflow,
# serp as google search tool, and pinecone as embedding index database all usint streamplit for web UI

import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        token = token.replace('"', '').replace(
            '{', '').replace('}', '').replace('_', ' ')
        self.text += token
        self.container.success(self.text)


# Initialize session states
open_api_key = os.environ.get('OPENAI_API_KEY')
pholder = st.empty()
with pholder.container():
    stream_handler = StreamHandler(pholder)

chat = ChatOpenAI(
    openai_api_key=open_api_key,
    temperature=0,
    model="gpt-3.5-turbo",
    streaming=True,
    callbacks=[stream_handler],
)
if upit := st.chat_input("Postavite pitanje"):
    izlaz = st.write(chat.predict(upit))


