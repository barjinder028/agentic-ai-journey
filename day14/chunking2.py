from dotenv import load_dotenv
from google import genai
from google.genai import types
import os


load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"]) 


def dot_product(a, b):
    total = 0
    for x, y in zip(a, b):
        total += x * y
    return total

def magnitude(v):
    return dot_product(v, v) ** 0.5

def cosine_similarity(a, b):
    return dot_product(a, b) / (magnitude(a) * magnitude(b))

document = """
The Great Wall of China is a series of fortifications built across the historical northern borders of China. Construction began over 2,000 years ago and continued through several dynasties. It stretches for thousands of kilometers.

The Eiffel Tower was completed in 1889 for the World's Fair in Paris. It was designed by Gustave Eiffel's engineering company. At the time, many Parisians criticized its design, though it later became a beloved landmark.

Mount Everest is the tallest mountain above sea level on Earth. It sits on the border between Nepal and Tibet. The first confirmed summit was achieved by Edmund Hillary and Tenzing Norgay in 1953.

The Amazon rainforest produces roughly 20 percent of the world's oxygen. It spans across nine countries in South America, with the majority located in Brazil. It's home to millions of species of plants and animals.
"""

chunks = []
for p in document.strip().split("\n\n"):                                                        
    chunks.append(p.strip())


chunk_embeddings = []

for c in chunks:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=c,
        config=types.EmbedContentConfig(output_dimensionality=10)
    )
    chunk_embeddings.append({"text": c, "embedding": result.embeddings[0].values})


def search(query, chunk_embeddings, top_n=1):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=10)
    )
    query_embedding = result.embeddings[0].values

    scored = []
    for item in chunk_embeddings:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append({"text": item["text"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def rag_answer(question, chunk_embeddings):
    results = search(question, chunk_embeddings, top_n=3)

    context = "\n\n".join([r["text"] for r in results])

    prompt = f"""Answer the question using ONLY the context below.
If the context does not actually contain the answer, say "I don't know based on the given context."
Do not use any outside knowledge.

Context:
{context}

Question: {question}"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

print(rag_answer("Which structure took centuries to build?", chunk_embeddings))
print(rag_answer("What is the capital of Japan?", chunk_embeddings))

"""
--------------------------------------------------------Output------------------------------------------------------------------

Based on the provided context, **the Great Wall of China** is the structure, as its construction began over 2,000 years ago and continued through several dynasties.

I don't know based on the given context.

"""