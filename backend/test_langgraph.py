# test_langgraph.py
try:
    from langgraph.graph import StateGraph
    print("LangGraph imported successfully!")

        # Test basic functionality
    graph = StateGraph()
    print("LangGraph instance created successfully!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
