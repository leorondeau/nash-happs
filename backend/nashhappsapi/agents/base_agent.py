import sys
import os
print(sys.path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

class BaseAgent:
    def __init__(self):
        pass

    def process(self, input_data):
        raise NotImplementedError("Subclasses must implement this method.")
