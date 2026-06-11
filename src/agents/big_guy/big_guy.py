"""
Each agent should preprocess input and postprocess output
"""

from src.agents.base_agent import BaseAgent

class Analyst(Agent):
    def __init__(self):
        super().__init__()

    def run(self, prompt):
        prompt = [
            {
                "role": "system",
                "content": "You are a data visualisation specialist. You will look at the raw input data as a CSV as well as a quick summary of the important features, and then describe what the most effective chart is."
            },
            {
                "role": "user",
                "content": prompt
            },
        ]

        
        

    def fine_tune(self):
        ...