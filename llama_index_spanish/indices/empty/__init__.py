"""Empty Index."""

from llama_index_spanish.indices.empty.base import EmptyIndex, GPTEmptyIndex
from llama_index_spanish.indices.empty.retrievers import EmptyIndexRetriever

__all__ = ["EmptyIndex", "EmptyIndexRetriever", "GPTEmptyIndex"]
