from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import tools
from dotenv import load_dotenv
import os
load_dotenv("gapi.env")

# initialising the model
model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0, 
        openai_api_key=os.getenv("OPENAI_KEY"),
    )

# creating the tools for tool calling
api_tools = [getattr(tools,i) for i in dir(tools) if i.startswith('tool')]
api_tools = [tool(i) for i in api_tools]

# setting core system prompt
system_message = """You are an agent developed by Expedite Commerce to analyze stock data over a period of time.
"""
memory = MemorySaver()

# react agent app to call tools according to LLM understanding
app = create_react_agent(
    model, api_tools, state_modifier=system_message, checkpointer=memory
)
