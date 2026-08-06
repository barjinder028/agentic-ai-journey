from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import date
from tools import get_today_date, add_numbers
import os

load_dotenv()

class Agent:                                                                            # define the Agent class
    def __init__(self):                                                                 
        self.history = []                                                               # self.history is a list that will store the conversation history between the user and the model
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])                # Initialize the Gemini client with the API key
        self.tools = [get_today_date, add_numbers]                                      # self.tools is a list that contains the functions get_today_date and add_numbers, which can be used by the model to perform specific tasks
    
    def send(self, message):                                                            # define the send method that takes a message as input
        self.history.append({"role": "user", "parts": [{"text": message}]})             # Append the user's message to the conversation history with the role "user"

        response = self.client.models.generate_content(                                 # Call the generate_content method of the Gemini client to generate a response from the model
            model="gemini-3.5-flash",
            contents= self.history,
            config=types.GenerateContentConfig(tools= self.tools)
        )


        self.history.append({"role": "model", "parts": [{"text": response.text}]})     # Append the model's response to the conversation history with the role "model"
        return response.text                                                           # Return the text of the model's response


agent = Agent()                                                                        # create an instance of the Agent class
print(agent.send("My name is Barji."))                                                 # send a message to the agent and print the response
print(agent.send("What's today's date?"))
print(agent.send("Add 15 and 27, then tell me if that number is bigger than today's day of the month."))
print(agent.send("What's my name, and what was the sum you calculated?"))



---------------------------------output---------------------------------

"""
Hello Barji! How can I help you today?
Today's date is 2026-08-06.
The sum of 15 and 27 is 42. Today's day of the month is the 6th. 42 is bigger than 6.
Your name is Barji, and the sum I calculated was 42.
"""