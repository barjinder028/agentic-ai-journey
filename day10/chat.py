from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import date
import os

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def get_today_date():
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b

available_tools = {                                                                         #list of available tools for the agent to use
    "get_today_date": get_today_date,
    "add_numbers": add_numbers
}

def run_agent(question):                                                                    #defines the function to run the agent with a given question
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]    #constructs the initial content for the agent with the user's question

    while True:                                                                             #continues to generate responses until a final answer is produced
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=list(available_tools.values()),                                                       #provides the list of available tools to the model
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)               #disables automatic function calling, allowing the model to decide when to call functions
            )
        )

        if not response.function_calls:                                                                     #condition to check if the model has made any function calls; if not, it returns the final response text
            return response.text

        contents.append(response.candidates[0].content)                                                     #appends the model's response to the contents list for further processing

        function_response_parts = []                                                                        #initializes an empty list to store the responses from the function calls made by the model
        for function_call in response.function_calls:                                                       #iterates through each function call made by the model, retrieves the corresponding function from the available tools, executes it with the provided arguments, and appends the result to the function_response_parts list
            function_to_call = available_tools[function_call.name]
            result = function_to_call(**function_call.args)
            function_response_parts.append(
                types.Part.from_function_response(name=function_call.name, response={"result": result})     #creates a Part object representing the function response, including the function name and the result of the function call
            )

        contents.append(types.Content(role="tool", parts=function_response_parts))                          #appends the function responses to the contents list, allowing the model to see the results of its function calls and continue generating responses based on that information


print(run_agent("Get today's date, take the day number, add 100 to it, and tell me the result."))           #calls the run_agent function with a specific question, which prompts the model to get today's date, extract the day number, add 100 to it, and return the result. The final output is printed to the console.


"""
--------------------------------------------------output----------------------------------------------------------


Today's date is August 8, 2026. Taking the day number, which is 8, and adding 100 to it gives **108**.

"""