from langchain_core.tools import tool
from datetime import date
from dotenv import load_dotenv
from langchain.agents import create_agent


@tool
def get_today_date() -> str:
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the result."""
    return a + b



load_dotenv()

tools = [get_today_date, add_numbers]

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=tools,
    system_prompt="You are a helpful assistant."
)


response = agent.invoke({
    "messages": [{"role": "user", "content": "What is today's date, and what is 59 plus 97?"}]
})

print(response["messages"][-1].content)