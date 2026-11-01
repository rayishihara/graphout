import time
import mlflow

from transformers import AutoModelForCausalLM, AutoTokenizer
from src.agents.base_agent import BaseAgent
from src.agents.config import BaseAgentConfig


class BigGuy(BaseAgent):
    def __init__(
        self,
        tokenizer: AutoTokenizer,
        model: AutoModelForCausalLM,
        config: BaseAgentConfig,
    ) -> None:
        super().__init__(tokenizer, model, config)

    def run(self, message: str) -> str:
        prompt = [
            {
                "role": "system",
                "content": (
                    "You are a data visualisation specialist. You will read a summary of a dataset and its columns, "
                    "then choose the single most effective chart. "
                    "Respond with ONLY a JSON object with the keys \"chart_type\", \"x\", \"y\" and \"title\". "
                    "\"chart_type\" must be one of \"bar\", \"line\", \"scatter\" or \"histogram\". "
                    "\"x\" and \"y\" must be exact column names; set \"y\" to null for a histogram. "
                    "Do not include any other text."
                )
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

        with mlflow.start_run(run_name="big_guy_inference", nested=True):
            mlflow.log_param("user_message_preview", message[:200])

            start = time.time()
            response = self._generate(self._tokenize(prompt))
            latency = time.time() - start

            mlflow.log_param("response_preview", response[:200])

            mlflow.log_metric("latency_seconds", latency)
            mlflow.log_metric("prompt_length_chars", len(message))
            mlflow.log_metric("response_length_chars", len(response))

        return response
