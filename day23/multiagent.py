from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from datetime import date
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

load_dotenv()

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


@tool
def get_today_date() -> str:
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b
    


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


supervisor_model = model

workflow = create_supervisor(
    [date_agent, math_agent],
    model=supervisor_model,
    prompt="You are a supervisor managing two specialists: a date agent and a math agent. Route each question to whichever one can actually answer it."
)

app = workflow.compile()


response = app.invoke({
    "messages": [{"role": "user", "content": "What is today's date?"}]
})
print(response["messages"][-1].content)

response = app.invoke({
    "messages": [{"role": "user", "content": "What is 47 plus 89?"}]
})
print(response["messages"][-1].content)


response = app.invoke({
    "messages": [{"role": "user", "content": "What is today's date, and separately, what is 100 plus 250?"}]
})
print(response["messages"][-1].content)

"""
--------------------------------------------------------------output---------------------------------------------------------------------

Today's date is 2026-08-17.
136
Today's date is 2026-08-17.
100 + 250 = 350.

"""