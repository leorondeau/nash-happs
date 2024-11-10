# graph.py
from langgraph.graph import StateGraph, Node, ConditionalRouter
from agents.extract_agent import ExtractAgent
from agents.validate_agent import ValidateAgent
from state import ExtractState

# Instantiate the state
initial_state = ExtractState()

# Create instances of the agents
extract_agent = ExtractAgent()
validate_agent = ValidateAgent()

# Create nodes for the agents
extract_node = Node(agent=extract_agent, name="ExtractNode")
validate_node = Node(agent=validate_agent, name="ValidateNode")

# Create the state graph
graph = StateGraph(
    name="Extract and Validate Graph",
    start_node=extract_node,
    initial_state=initial_state
)

# Add nodes to the graph
graph.add_node(extract_node, name="ExtractNode")
graph.add_node(validate_node, name="ValidateNode")

# Define a router with conditional edges
router = ConditionalRouter(
    name="ValidationRouter",
    conditions=[
        (lambda state: state.text is not None, validate_node)  # Route to ValidateNode if text is extracted
    ],
    default=extract_node  # Default route if condition is not met (e.g., no extracted text)
)

# Add the router to the graph
graph.add_router(router)

# Connect the nodes to the router
graph.add_edge(extract_node, router)  # From ExtractNode to router
graph.add_edge(router, validate_node)  # From router to ValidateNode if condition is true

# Ensure the state is being passed through nodes
graph.set_state_passing(True)

# Optionally, visualize or execute the graph
if __name__ == "__main__":
    final_state = graph.run(initial_state)
    print("Final State:", final_state)
    print("Messages Log:", final_state['messages'])
