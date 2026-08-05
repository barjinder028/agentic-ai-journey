from dotenv import load_dotenv      # Load environment variables from a .env file
from google import genai            # Import the Google GenAI client library
from google.genai import types      # Import types for configuring the content generation
from datetime import date           # Import the date class from the datetime module

load_dotenv()                       
import os                           # Load the os module to access environment variables
from tools import get_today_date, add_numbers       # Import the required functions from tools.py

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])      # Initialize the GenAI client with the API


response = client.models.generate_content(                              #generate content using the GenAI client
    model="gemini-2.5-flash",                       
    contents="what is today's date?, and what is 59 plus 97?",          #prompt for the model to generate content
    config=types.GenerateContentConfig(                                 #configure the content generation with the tool to use
        tools=[get_today_date, add_numbers]
    )
)

print(response.text)                                                    #print the generated content response text


