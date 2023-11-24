from typing import Callable, List

from llama_index_spanish.bridge.pydantic import BaseModel
from llama_index_spanish.tools.types import BaseTool


class Task(BaseModel):
    message: str
    expected_response: str
    tools: List[BaseTool]
    eval_fn: Callable[[str, str], bool]

    class Config:
        arbitrary_types_allowed = True
