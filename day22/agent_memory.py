from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool
from datetime import date

load_dotenv()

@tool
def get_today_date() -> str:
    """Returns today's date as a string in YYYY-MM-DD format."""
    return str(date.today())

tools = [get_today_date]

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=tools,
    checkpointer=InMemorySaver()
)

thread_1 = {"configurable": {"thread_id": "conversation-1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Barji."}]},
    thread_1
)
print(response["messages"][-1].content)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    thread_1
)
print(response["messages"][-1].content)

thread_2 = {"configurable": {"thread_id": "conversation-2"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    thread_2
)
print(response["messages"][-1].content)


"""

---------------------------------------------------------------------Output---------------------------------------------------------------

[{'type': 'text', 'text': 'Nice to meet you, Barji! How can I help you today?', 'extras': {'signature': ....................'}}]
[{'type': 'text', 'text': 'Your name is Barji.', 'extras': {'signature': ........................'}}]
[{'type': 'text', 'text': "I don't know your name yet! Since I don't have access to your personal information, you'll have to tell me what it is. What should I call you?", 'extras': {'signature': ...............................}}]



""""