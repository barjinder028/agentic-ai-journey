from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json
import hashlib

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

chunks = [
    "The Great Wall of China is a series of fortifications built across the historical northern borders of China. Construction began over 2,000 years ago and continued through several dynasties. It stretches for thousands of kilometers.",

    "The Eiffel Tower was completed in 1889 for the World's Fair in Paris. It was designed by Gustave Eiffel's engineering company. At the time, many Parisians criticized its design, though it later became a beloved landmark.",

    "Mount Everest is the tallest mountain above sea level on Earth. It sits on the border between Nepal and Tibet. The first confirmed summit was achieved by Edmund Hillary and Tenzing Norgay in 1953.",

    "The Amazon rainforest produces roughly 20 percent of the world's oxygen. It spans across nine countries in South America, with the majority located in Brazil. It's home to millions of species of plants and animals."
]



def save_embeddings(chunk_embeddings, filename="embeddings.json"):
    with open(filename, "w") as f:
        json.dump(chunk_embeddings, f)


def get_chunks_hash(chunks):
    combined_text = "".join(chunks)
    return hashlib.sha256(combined_text.encode()).hexdigest()


def load_embeddings(filename="embeddings.json"):
    with open(filename, "r") as f:
        return json.load(f)


def get_or_create_embeddings(chunks, filename="embeddings.json"):
    current_hash = get_chunks_hash(chunks)

    if os.path.exists(filename):
        cached_data = load_embeddings(filename)
        if cached_data.get("hash") == current_hash:
            print("Loading cached embeddings...")
            return cached_data["chunk_embeddings"]
        else:
            print("Document changed, recomputing embeddings...")

    print("Computing embeddings...")
    chunk_embeddings = []
    for c in chunks:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=c
        )
        chunk_embeddings.append({"text": c, "embedding": result.embeddings[0].values})

    save_embeddings({"hash": current_hash, "chunk_embeddings": chunk_embeddings}, filename)
    return chunk_embeddings

chunk_embeddings = get_or_create_embeddings(chunks)



def search(query, chunk_embeddings, top_n=1):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
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



eval_set = [
    {"question": "How tall is the tallest mountain on Earth?", "expected_chunk_index": 2},
    {"question": "What year was a famous Parisian landmark completed?", "expected_chunk_index": 1},
    {"question": "How much oxygen does a rainforest produce?", "expected_chunk_index": 3},
    {"question": "How old are China's ancient fortifications?", "expected_chunk_index": 0},
    {"question": "Which structure took centuries to build?", "expected_chunk_index": 0},
]

def evaluate_retrieval(eval_set, chunks, chunk_embeddings, top_n=1):
    correct = 0

    for item in eval_set:
        results = search(item["question"], chunk_embeddings, top_n=top_n)
        retrieved_texts = [r["text"] for r in results]
        expected_text = chunks[item["expected_chunk_index"]]

        is_correct = expected_text in retrieved_texts
        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"{status} | {item['question']}")
        if not is_correct:
            print(f"   expected: {expected_text[:60]}")
            print(f"   got:      {retrieved_texts[0][:60]}")

    accuracy = correct / len(eval_set)
    return accuracy

accuracy_top1 = evaluate_retrieval(eval_set, chunks, chunk_embeddings, top_n=1)
print(f"Top-1 accuracy: {accuracy_top1 * 100:.0f}%")

"""
------------------------------------------------------------------output--------------------------------------------------------------------

1st run

Computing embeddings...
PASS | How tall is the tallest mountain on Earth?
PASS | What year was a famous Parisian landmark completed?
PASS | How much oxygen does a rainforest produce?
PASS | How old are China's ancient fortifications?
PASS | Which structure took centuries to build?
Top-1 accuracy: 100%

2nd run

Loading cached embeddings...
PASS | How tall is the tallest mountain on Earth?
PASS | What year was a famous Parisian landmark completed?
PASS | How much oxygen does a rainforest produce?
PASS | How old are China's ancient fortifications?
PASS | Which structure took centuries to build?
Top-1 accuracy: 100%


3rd run (changed 2000 to 3000 in the chunks list)

Document changed, recomputing embeddings...
Computing embeddings...
PASS | How tall is the tallest mountain on Earth?
PASS | What year was a famous Parisian landmark completed?
PASS | How much oxygen does a rainforest produce?
PASS | How old are China's ancient fortifications?
PASS | Which structure took centuries to build?
Top-1 accuracy: 100%


"""