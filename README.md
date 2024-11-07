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
