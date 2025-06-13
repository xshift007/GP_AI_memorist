class Agent:
    """Base class for all agents."""
    def __init__(self, name: str):
        self.name = name

    def run(self, input_data: str) -> str:
        """Process the input data and return a response."""
        raise NotImplementedError("Agents must implement the run method")
