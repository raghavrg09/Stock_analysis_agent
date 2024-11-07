# Stock_analysis_agent
The application consists of three main modules:

- agent
- tools
- app

## Agent
Agent is the core of the application which is responsible for tool calling through the LLM and providing the respective output.
It is a 'langgraph' based ReAct Agent which is capable of handling queries and performing/calling tools according to the user's query

## Tools
Tools is the script containing the custom tools to fetch and retreive data and calculate operations to analyze performance over a given period of time
As of now, there are only 3 tools:

- get the ticker symbols
- fetch and save stock data
- calculate returns over x number fo days

## App
App is nothing but a streamlit based application serving as UI to interact with the application using the LLM ReAct agent

## Workflow
Please run the main application using the requirements.txt file and command as:
```
streamlit run app.py
```
More number of tools can be added to the tools.py script as needed. 
#### Note: Please add OPENAI_API_KEY in the gapi.env file
