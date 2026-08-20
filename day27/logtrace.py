from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from google import genai
from datetime import date
import os

import json
import time

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


def log_trace(filename, entry):
    with open(filename, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_total_usage(response):
    total_input = 0
    total_output = 0

    for msg in response["messages"]:
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            total_input += usage["input_tokens"]
            total_output += usage["output_tokens"]

    return {"input_tokens": total_input, "output_tokens": total_output}


def traced_invoke(question, log_filename="trace_log.jsonl"):
    start_time = time.time()

    response = app.invoke({"messages": [{"role": "user", "content": question}]})

    elapsed = time.time() - start_time
    routed_agent = get_routed_agent(response)
    usage = get_total_usage(response)
    cost = calculate_cost(usage)

    entry = {
        "timestamp": time.time(),
        "question": question,
        "routed_agent": routed_agent,
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "cost": cost,
        "latency_seconds": round(elapsed, 3)
    }

    log_trace(log_filename, entry)
    return response


INPUT_COST_PER_MILLION = 0.25   # replace with the real number from Azure's pricing page
OUTPUT_COST_PER_MILLION = 2.00  # replace with the real number from Azure's pricing page

def calculate_cost(usage):
    input_cost = (usage["input_tokens"] / 1_000_000) * INPUT_COST_PER_MILLION
    output_cost = (usage["output_tokens"] / 1_000_000) * OUTPUT_COST_PER_MILLION
    return input_cost + output_cost

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


for item in eval_set:
    traced_invoke(item["question"])

print("Done, check trace_log.jsonl")


def analyze_trace_log(filename="trace_log.jsonl"):
    entries = []
    with open(filename, "r") as f:
        for line in f:
            entries.append(json.loads(line))

    by_agent = {}
    for e in entries:
        agent = e["routed_agent"]
        if agent not in by_agent:
            by_agent[agent] = {"count": 0, "total_cost": 0, "total_latency": 0}
        by_agent[agent]["count"] += 1
        by_agent[agent]["total_cost"] += e["cost"]
        by_agent[agent]["total_latency"] += e["latency_seconds"]

    for agent, stats in by_agent.items():
        avg_cost = stats["total_cost"] / stats["count"]
        avg_latency = stats["total_latency"] / stats["count"]
        print(f"{agent}: {stats['count']} calls, avg cost ${avg_cost:.6f}, avg latency {avg_latency:.2f}s")

analyze_trace_log()

"""
--------------------------------------------------------------output---------------------------------------------------------------------

Loading cached embeddings...
Done, check trace_log.jsonl
date_agent: 2 calls, avg cost $0.000857, avg latency 14.09s
math_agent: 2 calls, avg cost $0.000563, avg latency 9.45s
resume_agent: 6 calls, avg cost $0.001317, avg latency 13.93s

"""