"""Init params."""

from llama_index_spanish.program.predefined.evaporate.base import (
    DFEvaporateProgram,
    MultiValueEvaporateProgram,
)
from llama_index_spanish.program.predefined.evaporate.extractor import EvaporateExtractor

__all__ = [
    "EvaporateExtractor",
    "DFEvaporateProgram",
    "MultiValueEvaporateProgram",
]
