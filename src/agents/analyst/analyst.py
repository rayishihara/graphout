from transformers import AutoModelForCausalLM, AutoTokenizer

from src.agents.base_agent import BaseAgent
from src.agents.config import AnalystConfig

class Analyst(BaseAgent):
    def __init__(
        self,
        tokenizer: AutoTokenizer,
        model: AutoModelForCausalLM,
        config: AnalystConfig,
    ) -> None:
        super().__init__(tokenizer, model, config)

    def run(self, message: str) -> str:
        prompt = [
            {
                "role": "system",
                "content": "You are a data visualisation specialist. You will look at raw data in a CSV format and produce a summary of key features."
            },
            {
                "role": "user",
                "content": message
            },
        ]

        if self.adapter_name is not None:
            self.model.set_adapter(self.adapter_name)
        elif getattr(self.model, "_hf_peft_config_loaded", False):
            self.model.disable_adapters()  # Clear adapters, if at all used

        return self._generate(self._tokenize(prompt))

    def fine_tune(self):
        ...