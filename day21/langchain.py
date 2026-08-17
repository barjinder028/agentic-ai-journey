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

"""
-------------------------------------------------------------output--------------------------------------------------------------------
[{'type': 'text', 'text': "Today's date is August 17, 2026, and 59 plus 97 is 156.", 'extras': {'signature': 'EoMCCoACARFNMg/muJbijosWEI+ufuMSUUWihy4KUnwe5j+amNU8Gck4rQwF71CHz6IQddaZpQ3cwNG8NN3MFGJIUVw4Me37sOFsj2SsaTbWnSReJINfMKPtwHlG3wcyp3r1VtPk4v8PtswLR1S2tywoM1c3Ty+653xxY9ofzTBzseqURNkvnGhk2+bdjU8RSYpZyr5aWJ8DzAl0PqV793qhg/kf1nFv4bkiHQBRzLjXHqWJXjtWvDuqfoBkYwOf2p9mNASaKJ/czhDwjmcbE0x48RtqSajl09RxFjXCB7RcSscebcpa7Ok6NHryl0NesgZBrmO8LVL1lwc38MulOVq9vcTF0w=='}}]


-------------------------------------------------------------Note----------------------------------------------------------------------
This is the internal bookkeeping mechanism that the langchain and the LLM model use ({'signature':....) It is tied to a metadata that tells how the response is being generated. 

"""

