from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b

user_message = types.Content(
    role="user",
    parts=[types.Part.from_text(text="What is 59 plus 97?")]
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[user_message],
    config=types.GenerateContentConfig(
        tools=[add_numbers],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)           #disable automatic function calling so that the model will not call the tool automatically
    )
)

function_call = response.function_calls[0]                                                      #retrieve the function call from the model's response

result = add_numbers(**function_call.args)                                                      #call the tool with the arguments provided by the model


function_response_part = types.Part.from_function_response(                                     #create a function response part to send back to the model
    name=function_call.name,
    response={"result": result}
)

function_call_content = response.candidates[0].content                                          #create a content object for the function call to send back to the model

function_response_content = types.Content(                                                      #create a content object for the function response to send back to the model
    role="tool",
    parts=[function_response_part]
)

final_response = client.models.generate_content(                                                # send the function call and function response back to the model to get the final answer
    model="gemini-3.5-flash",
    contents=[user_message, function_call_content, function_response_content],
    config=types.GenerateContentConfig(tools=[add_numbers])
)

print(final_response.text)                                                                      #print the final response from the model, which should include the result of the addition



------------------------------------------output------------------------------------------
"""
59 plus 97 is 156.
"""