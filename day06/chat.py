from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

class ChatBot:                                                              #define a class called ChatBot
    def __init__(self):                                                     #initialize the ChatBot class
        self.history = []                                                   #history is a list that will store the conversation history
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])    #load the Google API key from the environment variable and create a client object

    def send(self, message):                                                #define a method called send that takes a message as input  
        self.history.append({"role": "user", "parts": [{"text": message}]})         #append the user's message to the history list with the role "user" and the message text

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.history
        )


        self.history.append({"role": "assistant", "parts": [{"text": response.text}]})      #append the assistant's response to the history list with the role "assistant" and the response text
        return response.text


bot = ChatBot()
print(bot.send("My name is Barji."))
print(bot.send("What is my name?"))
print(bot.send("What did I say my name was, and can you spell it backwards?"))

------------Output------------

""" 
Hello Barji! It's nice to meet you.
Your name is Barji.
You said your name was **Barji**.

Spelled backwards, that would be **ijraB**.
"""