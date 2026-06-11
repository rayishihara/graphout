from typing import Any
from pydantic import BaseModel

class BaseAgentConfig(BaseModel):
    name: str = "meta-llama/Llama-3.2-1B-Instruct"
    generate_config: dict[str, Any] = {
        "max_new_tokens": 256,
    }