import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph
from agents.extract_agent import ExtractAgent
from agents.validate_agent import ValidateAgent
from state.extract_state import ExtractState
from typing import Literal

# Instantiate the state
initial_state = ExtractState()

# Create instances of the agents
extract_agent = ExtractAgent()
validate_agent = ValidateAgent()

# Create the state graph
graph = StateGraph(
    name="Extract and Validate Graph",
    start_node=extract_agent,
    initial_state=initial_state
)

# Add nodes to the graph
graph.add_node(extract_agent, name="ExtractNode")
graph.add_node(validate_agent, name="ValidateNode")

# Define a router with conditional edges
# router = ConditionalRouter(
#     name="ValidationRouter",
#     conditions=[
#         (lambda state: state.text is not None, validate_agent)  # Route to ValidateNode if text is extracted
#     ],
#     default=extract_agent  # Default route if condition is not met (e.g., no extracted text)
# )

def router(initial_state):
    # This is the router
    messages = initial_state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return '__end__'
    return "continue"

# Add the router to the graph
graph.add_router(router)

# Connect the nodes to the router
graph.add_edge(extract_agent, router)  # From ExtractNode to router
graph.add_edge(router, validate_agent)  # From router to ValidateNode if condition is true

# Ensure the state is being passed through nodes
graph.set_state_passing(True)

# Optionally, visualize or execute the graph
if __name__ == "__main__":
    final_state = graph.run(initial_state)
    print("Final State:", final_state)
    print("Messages Log:", final_state['messages'])
