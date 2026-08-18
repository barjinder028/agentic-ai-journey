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

response = app.invoke({
    "messages": [{"role": "user", "content": "What did Barjinder do at Amazon?"}]
})
print(response["messages"][-1].content)

response = app.invoke({
    "messages": [{"role": "user", "content": "What is Barjinder's favorite food?"}]
})

for msg in response["messages"]:
    print(type(msg).__name__, "-", getattr(msg, "name", None), "-", str(msg.content)[:80])

response = app.invoke({
    "messages": [{"role": "user", "content": "What programming languages does Barjinder's resume say he knows besides Python?"}]
})
print(response["messages"][-1].content)

"""
--------------------------------------------------------------output---------------------------------------------------------------------

Loading cached embeddings...

Barjinder was a Quality Auditor (QA on ML‑Integrated Systems) at Amazon in Hyderabad from Jan 2020 to May 2025. Key contributions:
- Ran large-scale QA and audit workflows on ML‑integrated data systems, sustaining 96%+ accuracy.
- Drove a 25% reduction in recurring defects via root‑cause analysis and process improvements.
- Built systematic validation checks (including Regex‑based pattern checks) to catch errors before delivery.

HumanMessage - None - What is Barjinder's favorite food?
AIMessage - supervisor - 
ToolMessage - transfer_to_resume_agent - Successfully transferred to resume_agent
AIMessage - resume_agent - I don't know — Barjinder's resume does not mention a favorite food.
AIMessage - resume_agent - Transferring back to supervisor
ToolMessage - transfer_back_to_supervisor - Successfully transferred back to supervisor
AIMessage - supervisor - I don't know — Barjinder's resume does not mention a favorite food.

Besides Python, his resume lists SQL.

"""