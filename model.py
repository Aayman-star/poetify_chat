import time
from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run import Run
from dotenv import load_dotenv,find_dotenv
from typing import Any


class MessageContent:
    def __init__(self,role:str,msgstring:str| Any):
        self.role = role
        self.msgstring=msgstring


class ChatAssistant:
    def __init__(self,name:str,instructions:str,model="gpt-3.5-turbo-1106"):
        self.name :str = name;
        self.instructions:str = instructions;
        self.model:str = model;

        load_dotenv(find_dotenv());
        self.client : OpenAI = OpenAI();
        self.chat_assistant:Assistant = self.client.beta.assistants.create(
              name=self.name,
              model = self.model,
              instructions = self.instructions
           )
        """
        #Thread is being created
        """
        self.thread: Thread  = self.client.beta.threads.create()   
        self.messages: list[MessageContent] = []
       # self.add_message(MessageContent(role="user",msgstring=prompt))
       
        """
        #This fucntion will receive question from the user
        """
    def askquestion(self,question:str):
              latestthread: Thread = self.client.beta.threads.messages.create(
                    thread_id = self.thread.id,
                    role = "user",
                    content=question
              )
              """
              #Initiating the run of the thread
              """
              self.latest_run:Run = self.client.beta.threads.runs.create(
                       thread_id=self.thread.id,
                       assistant_id=self.chat_assistant.id,
                       instructions=self.instructions
              )
              self.add_message(MessageContent( role ="user",msgstring=question))
        
    """
    #This function will check the status of the run
    #When this fucntion returns true,it would mean that the run has been completed
    """
    def is_complete(self)->bool:
        print("Current Status-----",self.latest_run.status)
        while self.latest_run.status != "completed":
            time.sleep(1)
            self.latest_run:Run = self.client.beta.threads.runs.retrieve(
                  thread_id = self.thread.id,
                  run_id = self.latest_run.id

            )
            print("Latest Status: ", self.latest_run)
        return True
        
        
    """
    #Returning the thread id
    """
    def get_thread_id(self):
          return self.thread.id
    """
    #This function will get the answer to the current question
    """
    def get_answer(self)->MessageContent:
            response = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
            
            #print("Assistant:",answer.role,"Answet",answer.msgstring)
            print("Response: ", response.data[0])
            answer = MessageContent(response.data[0].role, response.data[0].content[0].text.value)
            self.add_message(answer)
            return answer.msgstring
            """
            #This function creates the message history by appending the message to the list of messages
            """
    def add_message(self,message)->None:
            self.messages.append(message)

            """
            #This is the entire message history to be displayed
            """
    def get_message_history(self)->list[MessageContent]:
            return self.messages

            
