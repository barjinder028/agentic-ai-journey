from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

response1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="My name is Barji."
)
print(response1.text)

response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is my name?"
)
print(response2.text)