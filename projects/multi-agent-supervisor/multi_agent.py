from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from google import genai
from datetime import date
import os

load_dotenv()

# Chat model: Azure
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

model = AzureChatOpenAI(
    azure_deployment="gpt-5-mini",
    api_version="2024-05-01-preview",
    azure_endpoint="https://barjinder0228-8766-resource.services.ai.azure.com/",
    azure_ad_token_provider=token_provider,
    max_retries=5,
)

# Embeddings client: Gemini, separate system, separate quota
genai_client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

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

def save_embeddings(chunk_embeddings, filename="embeddings.json"):
    import json
    with open(filename, "w") as f:
        json.dump(chunk_embeddings, f)

def load_embeddings(filename="embeddings.json"):
    import json
    with open(filename, "r") as f:
        return json.load(f)

def get_chunks_hash(chunks):
    import hashlib
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
        result = genai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=c
        )
        chunk_embeddings.append({"text": c, "embedding": result.embeddings[0].values})

    save_embeddings({"hash": current_hash, "chunk_embeddings": chunk_embeddings}, filename)
    return chunk_embeddings

def search(query, chunk_embeddings, top_n=1):
    result = genai_client.models.embed_content(
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

def get_routed_agent(response):
    for msg in response["messages"]:
        name = getattr(msg, "name", None)
        if name in ["date_agent", "math_agent", "resume_agent"]:
            return name
    return "supervisor"

# Load resume and build/load embeddings
chunks = load_document("my_document.txt")
chunk_embeddings = get_or_create_embeddings(chunks, filename="my_document_embeddings.json")

# Tools
@tool
def get_today_date() -> str:
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b

@tool
def search_resume(question: str) -> str:
    """Searches Barjinder's resume for information relevant to the question. Returns the most relevant excerpts."""
    results = search(question, chunk_embeddings, top_n=3)
    return "\n\n".join([r["text"] for r in results])

# Agents
date_agent = create_agent(
    model=model,
    tools=[get_today_date],
    name="date_agent",
    system_prompt="You are a specialist that only answers questions about dates. If asked anything else, say it's outside your area."
)

math_agent = create_agent(
    model=model,
    tools=[add_numbers],
    name="math_agent",
    system_prompt="You are a specialist that only performs arithmetic. If asked anything else, say it's outside your area."
)

resume_agent = create_agent(
    model=model,
    tools=[search_resume],
    name="resume_agent",
    system_prompt="""You are a specialist that answers questions about Barjinder's resume.
Use the search_resume tool to find relevant information, then answer using ONLY what it returns.
If the tool's results don't contain the answer, say you don't know, rather than guessing.
If asked about anything unrelated to the resume, say it's outside your area."""
)

# Supervisor
workflow = create_supervisor(
    [date_agent, math_agent, resume_agent],
    model=model,
    prompt="""You are a supervisor managing three specialists: a date agent, a math agent, and a resume agent.

Route each question to whichever specialist can actually answer it. Any question that mentions Barjinder, or could plausibly be answered by looking at his resume, should go to the resume agent, even if you personally don't know the answer. Never answer a question yourself if one of your specialists might have relevant information. Only answer directly if the question clearly needs none of the three specialists."""
)

app = workflow.compile()


eval_set = [
    {"question": "What is today's date?", "expected_agent": "date_agent"},
    {"question": "What is 15 plus 27?", "expected_agent": "math_agent"},
    {"question": "What did Barjinder do at Amazon?", "expected_agent": "resume_agent"},
    {"question": "What is Barjinder's favorite food?", "expected_agent": "resume_agent"},
    {"question": "What programming languages does Barjinder know?", "expected_agent": "resume_agent"},
]


def evaluate_routing(eval_set):
    correct = 0

    for item in eval_set:
        response = app.invoke({
            "messages": [{"role": "user", "content": item["question"]}]
        })
        actual_agent = get_routed_agent(response)
        is_correct = actual_agent == item["expected_agent"]
        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"{status} | {item['question']}")
        print(f"   expected: {item['expected_agent']}, got: {actual_agent}")

    accuracy = correct / len(eval_set)
    return accuracy


accuracy = evaluate_routing(eval_set)
print(f"Routing accuracy: {accuracy * 100:.0f}%")

"""
--------------------------------------------------------------output---------------------------------------------------------------------

Loading cached embeddings...
PASS | What is today's date?
   expected: date_agent, got: date_agent
PASS | What is 15 plus 27?
   expected: math_agent, got: math_agent
PASS | What did Barjinder do at Amazon?
   expected: resume_agent, got: resume_agent
PASS | What is Barjinder's favorite food?
   expected: resume_agent, got: resume_agent
PASS | What programming languages does Barjinder know?
   expected: resume_agent, got: resume_agent
Routing accuracy: 100%

"""