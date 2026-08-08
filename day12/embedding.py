from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

sentences = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "Stock prices fell sharply today."
]


for s in sentences:                                                                         
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=s,
        config=types.EmbedContentConfig(output_dimensionality=10)                       #set output_dimensionality to 10 to match the cosine similarity example
    )
    print(s)                                                                            #print the original sentence
    print(result.embeddings[0].values)                                                  #print the embedding values
    print()                                                                             #print a blank line for better readability

"""
-----------------------------------------------------output-----------------------------------------------------

The cat sat on the mat.
[-0.022607181, 0.015246871, 0.001684601, -0.0769077, 0.0045841224, 0.004410481, 0.002776919, 0.011506936, 0.005208321, 0.019448007]

A feline rested on the rug.
[-0.02797855, 0.02481298, -0.016868742, -0.08025024, -0.002099059, -0.0050075497, 0.021626232, 0.019801918, -0.004602447, 0.0064060204]

Stock prices fell sharply today.
[0.015420642, 0.014837707, -0.016661834, -0.06344831, -0.009507145, 0.027634429, -0.008880608, -0.014410841, -0.017238302, 0.024441158]


""""