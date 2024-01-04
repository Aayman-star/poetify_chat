import os
from dotenv import find_dotenv,load_dotenv
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from model import MessageContent,ChatAssistant
import streamlit as st
_bool = load_dotenv()

my_string = os.environ["DATABASE_URL"];

st.title("Poetify--your chatty friend")
st.write("Your poetic assistant!")

#??This is where the engine is being created

engine:Engine = create_engine(my_string)

#??This function is to insert data in the database
def insert_data(question:str,answer:str):
    with engine.begin() as conn:
         conn.execute(text("CREATE TABLE IF NOT EXISTS chat_history (question TEXT, answer TEXT)"))
         conn.execute(text("INSERT INTO chat_history (question, answer) VALUES (:question, :answer)"),
        [{"question": question, "answer": answer}]
        
        )
#??This function retrives data from the database and displays it as a conversation history
def retrieve_data():
    with engine.begin() as conn:
        table = conn.execute(text("SELECT * FROM chat_history"));
        #st.markdown(type(table))
        if table.rowcount > 0:
            for row in table:
                with st.chat_message("user"):
                    st.markdown(row.question)
                with st.chat_message("assistant"):
                    st.markdown(row.answer)

            #st.write("user:",row.question,"assistant:",row.answer)
        else:
            st.write("No history to show")

#??This function will delete the history from the database  

def delete_data():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM chat_history"));


#??Defining the assistant
instructions:str = """You are a poetic assistant, skilled in responding to 
                      the questions from all fields of life with a poetic flair"""
name : str = 'Poetic Assistant'
if "chat_assistant" not in st.session_state:
    st.session_state.chat_assistant = ChatAssistant(name,instructions) 

#??This is to display the current running thread of conversation

if "messages" not in st.session_state:
     st.session_state.messages = []

for m in st.session_state.chat_assistant.get_message_history():
    with st.chat_message(m.role):
        st.markdown(m.msgstring)

if prompt := st.chat_input("Please Ask a Question"):
    with st.chat_message("user"):
         st.markdown(prompt)
         st.session_state.chat_assistant.askquestion(prompt)
        
 
       
   
    with st.spinner('Searching for answer'):
        if(st.session_state.chat_assistant.is_complete()):
                response  = st.session_state.chat_assistant.get_answer()
                
    with st.chat_message("assistant"):
        st.markdown(response)
                      

    insert_data(prompt,response)
   


#??The conversation history in the sidebar
with st.sidebar:
    st.title("Conversation History")
    if st.button(":wastebasket:"):
         delete_data();
    retrieve_data()
    