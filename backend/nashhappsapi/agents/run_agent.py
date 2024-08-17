from langgraph_config import configure_workflow

def run():
    graph = configure_workflow()
    graph.run()

if __name__ == "__main__":
    run()
