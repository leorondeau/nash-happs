import os
import openai
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

# Load environment variables for Azure OpenAI credentials
load_dotenv()

openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')
openai.api_type = "azure"
openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
openai.api_version = os.getenv('API_VERSION')

# Define the tools for the agent to use
@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

tools = [search]

tool_node = ToolNode(tools)

# Function to invoke Azure OpenAI model
def call_azure_openai(messages):
    """Call the Azure OpenAI model with a list of messages."""
    azure_response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",  # Replace with your actual deployment name
        messages=messages,
        max_tokens=50,
        temperature=0  # Adjust if needed
    )
    return azure_response['choices'][0]['message']['content']

# Replace the model definition using Azure OpenAI
def call_model(state: MessagesState):
    messages = state['messages']
    # Prepare messages in the format required by Azure OpenAI
    formatted_messages = [{"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content} for m in messages]
    
    # Get response from the Azure model
    response_content = call_azure_openai(formatted_messages)
    
    # Return the response message wrapped in the expected format
    return {"messages": [HumanMessage(content=response_content)]}

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

# Define a new graph
workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", 'agent')

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable.
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile(checkpointer=checkpointer)

# Use the Runnable
final_state = app.invoke(
    {"messages": [HumanMessage(content="what is the weather in sf")]},
    config={"configurable": {"thread_id": 42}}
)

# Print the final response
print(final_state["messages"][-1].content)
