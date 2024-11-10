class BaseAgent:
    def __init__(self):
        pass

    def process(self, input_data):
        raise NotImplementedError("Subclasses must implement this method.")
