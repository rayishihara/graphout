from typing import Any
from pydantic import BaseModel, model_validator

class BaseAgentConfig(BaseModel):
    name: str = "meta-llama/Llama-3.2-1B-Instruct"

    adapter_name: str | None = None
    adapter_path: str | None = None

    @model_validator(mode="after")
    def check_adapter_fields_both_set(self) -> "BaseAgentConfig":
        path_set = self.adapter_path is not None
        name_set = self.adapter_name is not None
        if path_set != name_set:
            missing = "adapter_name" if path_set else "adapter_path"
            provided = "adapter_path" if path_set else "adapter_name"
            raise ValueError(
                f"'{missing}' must be set when '{provided}' is provided. "
                "Both adapter_path and adapter_name must be set together, or neither."
            )
        return self

    tokenize_config: dict[str, Any] = {
        "tokenize": True, 
        "add_generation_prompt": True,
        "return_tensors": "pt"
    }

    generate_config: dict[str, Any] = {
        "max_new_tokens": 256,
    }

class AnalystConfig(BaseAgentConfig):
    generate_config: dict[str, Any] = {
        "max_new_tokens": 32,
    }

