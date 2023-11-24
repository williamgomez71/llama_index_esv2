"""Vector-store based data structures."""

from llama_index_spanish.indices.multi_modal.base import MultiModalVectorStoreIndex
from llama_index_spanish.indices.multi_modal.retriever import MultiModalVectorIndexRetriever

__all__ = [
    "MultiModalVectorStoreIndex",
    "MultiModalVectorIndexRetriever",
]
