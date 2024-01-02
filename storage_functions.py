import os

import dotenv
from dotenv import load_dotenv,find_dotenv
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

"""
#Extracting the database string
"""
load_dotenv()
conn_str = os.getenv("DATABASE_URL")

"""
#This function is to add the conversation history to the database
"""
def add_convo(prompt:str,answer:str):
        engine: Engine = create_engine(conn_str)
        with engine.begin() as conn:
          conn.execute(text("CREATE TABLE IF NOT EXISTS chat_history (question TEXT, answer TEXT)"))
          conn.execute(text("INSERT INTO chat_history (question, answer) VALUES (:question, :answer)"),
        [{"question": prompt, "answer": answer}],
        )

def display_chat():
     engine: Engine = create_engine(conn_str)
      
     with engine.begin() as conn:
        my_table = conn.execute(text("SELECT * FROM chat_history"));
    
        my_table = pd.DataFrame(my_table)
    #print(my_table)
        rows,cols = my_table.shape
    #print(rows,cols)
        if rows > 0 : 
            for i in range(rows):
                print(my_table.at[i,"question"],"------------",my_table.at[i,"answer"])
                # return my_table.at[i,"question"],my_table.at[i,"answer"]
                return my_table
        else:
            print("Conversation History not found")
            return "No Conversation History"
     

"""
#Deleting the conversation
"""
def delete_convo():
    engine: Engine = create_engine(conn_str)
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM chat_history"));
