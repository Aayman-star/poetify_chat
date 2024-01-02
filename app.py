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


# def add_convo(prompt:str,answer:str):
#         engine: Engine = create_engine(conn_str)
#         with engine.begin() as conn:
#           conn.execute(text("CREATE TABLE IF NOT EXISTS chat_history (question TEXT, answer TEXT)"))
#           conn.execute(text("INSERT INTO chat_history (question, answer) VALUES (:question, :answer)"),
#         [{"question": prompt, "answer": answer}],
#         )
          
# def display_chat():
#      engine: Engine = create_engine(conn_str)
      
#      with engine.begin() as conn:
#         my_table = conn.execute(text("SELECT * FROM chat_history"));
#         my_table = pd.DataFrame(my_table)
#     #print(my_table)
#         rows,cols = my_table.shape
#     #print(rows,cols)
#         if rows > 0 : 
#             for i in range(rows):
#                 print(my_table.at[i,"question"],"------------",my_table.at[i,"answer"])
#                 with st.chat_message("user"):
#                      st.markdown(my_table.at[i,"question"])
#                 with st.chat_message("assistant"):
#                       st.markdown(my_table.at[i,"answer"])
                     
#         else:
#             st.markdown("No Conversation history")


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

