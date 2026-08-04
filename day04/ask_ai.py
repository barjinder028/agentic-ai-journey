from dotenv import load_dotenv
from google import genai
import os


load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def ask(question):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=question
)

    return(response.text)

print(ask("What's the capital of france?"))
print(ask("Name one python data type."))
print(ask("what year is it?"))


