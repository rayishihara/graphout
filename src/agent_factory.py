import os
import yaml
# from accelerator import Accelerator
from transformers import AutoModelForCausalLM, AutoTokenizer

# TODO: Use accelerator to send the model to GPU if available

class AgentFactory:
    def __init__(self) -> None:
        self._tokenizer_cache: dict = {}
        self._model_cache: dict = {}

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}

    def _get_tokenizer_and_model(self, config):
        model_name = config.name
        if model_name not in self._model_cache:
            self._tokenizer_cache[model_name] = AutoTokenizer.from_pretrained(model_name)
            self._model_cache[model_name] = AutoModelForCausalLM.from_pretrained(model_name)

        tokenizer = self._tokenizer_cache[model_name]
        model = self._model_cache[model_name]
        
        if config.adapter_path is not None:
            model.load_adapter(config.adapter_path, adapter_name=config.adapter_name)
            # It looks for adapter_config.json and adapter_model.safetensors at the path
            # This should be my local mlflow artifact folder

        return tokenizer, model

    def create_analyst(self):
        from src.agents.analyst.analyst import Analyst
        from src.agents.config import AnalystConfig
    
        config_path = os.path.join("src", "agents", "analyst", "analyst.yaml")
        config = AnalystConfig(**self._load_config(config_path))
        
        tokenizer, model = self._get_tokenizer_and_model(config)
    
        return Analyst(tokenizer, model, config)