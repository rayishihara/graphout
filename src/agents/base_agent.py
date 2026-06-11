from abc import ABC, abstractmethod
from accelerate import Accelerator
from src.agents.config import BaseAgentConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

class BaseAgent(ABC):
    def __init__(
        self,
        tokenizer: AutoTokenizer,
        model: AutoModelForCausalLM,
        config: BaseAgentConfig,
    ) -> None:
        self.tokenizer = tokenizer
        self.model = model

        self.generate_config = config.generate_config

    def _tokenize(self, prompt):
        return self.tokenizer.apply_chat_template(
            prompt, 
            tokenize=True, 
            add_generation_prompt=True,
            return_tensors="pt"
        )

    def _generate(self, tokenized_prompt):
        response = self.model.generate(
            **tokenized_prompt,
            **generate_config,
        )

    def _decode(self) ->:
        generated_tokens = response[0][tokenized_prompt.shape[-1]:]
        return self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

    @abstractmethod
    def run(self) -> something:
        raise NotImplementedError("Override this method")