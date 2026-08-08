from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import date
import os

load_dotenv()

def get_today_date():
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b

class Agent:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        self.available_tools = {
            "get_today_date": get_today_date,
            "add_numbers": add_numbers
        }
        self.history = []

    def send(self, message):
        self.history.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))

        max_rounds = 10                                                                                         #maximum number of rounds to prevent infinite loops
        rounds = 0                                                                                              #initialize rounds counter

        while rounds < max_rounds:                                                                              #while loop to allow multiple rounds of interaction with the model
            rounds += 1

            response = self.client.models.generate_content(                                                     #response from the model based on the current history and available tools
                model="gemini-3.5-flash",
                contents=self.history,
                config=types.GenerateContentConfig(
                    tools=list(self.available_tools.values()),
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                )
            )

            if not response.function_calls:                                                                     #if the model does not request any function calls, append the response to history and return the text
                self.history.append(response.candidates[0].content)
                return response.text

            self.history.append(response.candidates[0].content)                                               #append the model's response to the history, even if it includes function calls

            function_response_parts = []                                                                      #list to hold the results of the function calls made by the model
            for function_call in response.function_calls:                                                     #loop through each function call requested by the model and execute it, appending the results to the function_response_parts list
                try:                                                                                          #try to call the function and append the result to the function_response_parts list, if an error occurs, append the error message instead
                    function_to_call = self.available_tools[function_call.name]                               
                    result = function_to_call(**function_call.args)
                    function_response_parts.append(
                        types.Part.from_function_response(name=function_call.name, response={"result": result})
                    )
                except Exception as e:
                    function_response_parts.append(
                        types.Part.from_function_response(name=function_call.name, response={"error": str(e)})
                    )

            self.history.append(types.Content(role="tool", parts=function_response_parts))                   #append the results of the function calls to the history as a tool response

        return "I couldn't finish this within the allowed number of steps."                                  #return a message indicating that the model couldn't finish the task within the allowed number of steps



agent = Agent()                                                                                              #run the agent and test it with some example messages
print(agent.send("My name is Barji."))
print(agent.send("Get today's date, take the day number, and add 50 to it."))
print(agent.send("What's my name, and what was that final number?"))


"""
-----------------------------------------------output-----------------------------------------------

Nice to meet you, Barji! How can I help you today?
Today's date is **August 8, 2026**. 

Taking the day number, which is **8**, and adding 50 to it gives **58**.
Your name is **Barji**, and the final number we calculated was **58**.

"""