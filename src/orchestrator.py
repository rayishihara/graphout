from src.agent_factory import AgentFactory

class Orchestrator:
    def __init__(self) -> None:
        factory = AgentFactory()
        self.analyst = factory.create_analyst()
        # More agents later

    def run(self, message: str) -> str:
        return self.analyst.run(message)