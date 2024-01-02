import streamlit as st
# import os
# from dotenv import find_dotenv,load_dotenv
# from sqlalchemy.engine.base import Engine
# from sqlalchemy import create_engine
# from sqlalchemy import text
import pandas as pd
from model import MessageContent,ChatAssistant
from storage_functions import add_convo,display_chat,delete_convo

# load_dotenv()
# conn_str = os.getenv("DATABASE_URL")
with st.container():
    st.title("Poetify--your chatty friend")
    st.write("Your poetic assistant!")


with st.sidebar:
    st.title("Previous Conversations")
    x = st.button(':wastebasket:')
    if x:
        y = st.sidebar.checkbox('Are you sure you want to delete the coversation history?')
        if y:
             delete_convo()
    display_chat()
          
            
    text = display_chat()
    if isinstance(text,pd.DataFrame):
        rows,cols = text.shape
        for i in range(rows):
            with st.chat_message("user"):
                st.markdown(text.at[i,"question"])
            with st.chat_message("assistant"):
                st.markdown(text.at[i,"answer"])
    else:
         st.markdown("No conversation history to show")
    #display_chathistory()


instructions:str = """You are a poetic assistant, skilled in responding to 
                      the questions from all fields of life with a poetic flair"""
name : str = 'Poetic Assistant'
if "chat_assistant" not in st.session_state:
    st.session_state.chat_assistant = ChatAssistant(name,instructions)

if "messages" not in st.session_state:
     st.session_state.messages = []

for m in st.session_state.chat_assistant.get_message_history():
    with st.chat_message(m.role):
        st.markdown(m.msgstring)



if prompt := st.chat_input("Please Ask a Question"):
    with st.chat_message("user"):
         st.markdown(prompt)
         st.session_state.chat_assistant.askquestion(prompt)
         #chat_history = {"role":"user","content":prompt}
         #add_conversation("user",prompt)
 
       
   
    with st.spinner('Searching for answer'):
        if(st.session_state.chat_assistant.is_complete()):
                response  = st.session_state.chat_assistant.get_answer()
                
                with st.chat_message("assistant"):
                        st.markdown(response)
                        #add_conversation("assistant",response)

                add_convo(prompt,response)

