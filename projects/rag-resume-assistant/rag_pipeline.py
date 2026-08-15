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


def load_document(filename):
    with open(filename, "r") as f:
        text = f.read()
    return [p.strip() for p in text.strip().split("\n\n") if p.strip()]


chunks = load_document("my_document.txt")

print(f"Loaded {len(chunks)} chunks")
for i, c in enumerate(chunks):
    print(f"--- chunk {i} ---")
    print(c[:100])
    print()

def save_embeddings(chunk_embeddings, filename="embeddings.json"):
    with open(filename, "w") as f:
        json.dump(chunk_embeddings, f)



def load_embeddings(filename="embeddings.json"):
    with open(filename, "r") as f:
        return json.load(f)


def get_chunks_hash(chunks):
    combined_text = "".join(chunks)
    return hashlib.sha256(combined_text.encode()).hexdigest()



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

chunk_embeddings = get_or_create_embeddings(chunks, filename="my_document_embeddings.json")


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
    {"question": "Does Barjinder know Python?", "expected_text_contains": ["Python"]},
    {"question": "What did Barjinder do at Amazon?", "expected_text_contains": ["Amazon"]},
]

def evaluate_retrieval(eval_set, chunk_embeddings, top_n=1):
    correct = 0

    for item in eval_set:
        results = search(item["question"], chunk_embeddings, top_n=top_n)
        retrieved_texts = [r["text"] for r in results]
        combined_retrieved = " ".join(retrieved_texts)

        is_correct = any(phrase in combined_retrieved for phrase in item["expected_text_contains"])
        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"{status} | {item['question']}")

    accuracy = correct / len(eval_set)
    return accuracy

results = search("What work experience does the candidate from amazon?", chunk_embeddings, top_n=5)

for r in results:
    print(round(r["score"], 3), "-", r["text"][:100])


accuracy = evaluate_retrieval(eval_set, chunk_embeddings, top_n=1)
print(f"Top-1 accuracy on real document: {accuracy * 100:.0f}%")


accuracy_top3 = evaluate_retrieval(eval_set, chunk_embeddings, top_n=3)
print(f"Top-3 accuracy on real document: {accuracy_top3 * 100:.0f}%")


"""
------------------------------------------------------------------output--------------------------------------------------------------------

Loaded 17 chunks
--- chunk 0 ---
BARJINDER SINGH
Agentic AI Engineer
LangChain · LangGraph · RAG · Multi-Agent Systems · MCP · Python

--- chunk 1 ---
Hoshiarpur, Punjab, India  |  +91 7009628562  |  barjinder028@gmail.com
GitHub: github.com/barjinder

--- chunk 2 ---
SUMMARY:
Agentic AI Engineer with a hands-on foundation in Python, LLM
applications, and autonomous 

--- chunk 3 ---
CORE COMPETENCIES:
Agentic AI & LLMs
LLM Application Development · Tool / Function Calling · Agent L

--- chunk 4 ---
Frameworks & Protocols
LangChain · LangGraph · OpenAI Agents SDK ·
Model Context Protocol (MCP) · RA

--- chunk 5 ---
Retrieval & RAG
Embeddings · Vector / Cosine-Similarity Search · Document Chunking ·
Grounded Genera

--- chunk 6 ---
Programming & Cloud
Python · SQL · REST APIs · Git · Microsoft Azure · Azure AI

--- chunk 7 ---
Engineering Practices
Test Automation · Root Cause Analysis · Evaluation Harnesses ·
Debugging · Fai

--- chunk 8 ---
PROJECTS:
Custom Agent Framework - agentic-ai-journey            (Python · OpenAI SDK)
  - Built an 

--- chunk 9 ---
RAG Pipeline with Evaluation Harness                   (Python · Embeddings)
  - Built a retrieval-a

--- chunk 10 ---
RAG HR Assistant & Multi-Agent Procurement Workflow    (LangChain · LangGraph)
  - Building a RAG-po

--- chunk 11 ---
PROFESSIONAL EXPERIENCE:

--- chunk 12 ---
Senior Cloud Engineer - AI Quality Evaluation          May 2025 - Jan 2026
LTIMindtree (LTM)
  - Eva

--- chunk 13 ---
Quality Auditor - QA on ML-Integrated Systems          Jan 2020 - May 2025
Amazon, Hyderabad
  - Ran

--- chunk 14 ---
Senior Data Associate - Quality & Data Operations      Jun 2018 - Dec 2019
Wipro, Hyderabad
  - Perf

--- chunk 15 ---
CERTIFICATIONS:
  - Oracle Agentic AI Certified Foundations Associate
  - IBM - Make Agentic AI Work

--- chunk 16 ---
EDUCATION
Bachelor of Technology, Mechanical Engineering                     2017
Punjab Technical U

Document changed, recomputing embeddings...
Computing embeddings...
0.67 - PROFESSIONAL EXPERIENCE:
0.666 - Quality Auditor - QA on ML-Integrated Systems          Jan 2020 - May 
0.655 - Senior Cloud Engineer - AI Quality Evaluation          May 2025 - Jan 
0.615 - SUMMARY:
Agentic AI Engineer with a hands-on foundation in Python, LLM
0.586 - RAG Pipeline with Evaluation Harness                   (Python · Embed
PASS | Does Barjinder know Python?
FAIL | What did Barjinder do at Amazon?
Top-1 accuracy on real document: 50%
PASS | Does Barjinder know Python?
PASS | What did Barjinder do at Amazon?
Top-3 accuracy on real document: 100%


"""