from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState

#Create nodes and agents
#an extract agent and a validate agent
#tools: scraper, image extract, file read, ability to save to the db

#Next steps
#Scrape one post that has the image with dates before adding logic that searches all posts
