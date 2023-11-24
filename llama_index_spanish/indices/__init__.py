"""LlamaIndex data structures."""

# indices
from llama_index_spanish.indices.composability.graph import ComposableGraph
from llama_index_spanish.indices.document_summary import (
    DocumentSummaryIndex,
    GPTDocumentSummaryIndex,
)
from llama_index_spanish.indices.document_summary.base import DocumentSummaryIndex
from llama_index_spanish.indices.empty.base import EmptyIndex, GPTEmptyIndex
from llama_index_spanish.indices.keyword_table.base import (
    GPTKeywordTableIndex,
    KeywordTableIndex,
)
from llama_index_spanish.indices.keyword_table.rake_base import (
    GPTRAKEKeywordTableIndex,
    RAKEKeywordTableIndex,
)
from llama_index_spanish.indices.keyword_table.simple_base import (
    GPTSimpleKeywordTableIndex,
    SimpleKeywordTableIndex,
)
from llama_index_spanish.indices.knowledge_graph import (
    GPTKnowledgeGraphIndex,
    KnowledgeGraphIndex,
)
from llama_index_spanish.indices.list import GPTListIndex, ListIndex, SummaryIndex
from llama_index_spanish.indices.list.base import GPTListIndex, ListIndex, SummaryIndex
from llama_index_spanish.indices.loading import (
    load_graph_from_storage,
    load_index_from_storage,
    load_indices_from_storage,
)
from llama_index_spanish.indices.managed.vectara import VectaraIndex
from llama_index_spanish.indices.multi_modal import MultiModalVectorStoreIndex
from llama_index_spanish.indices.struct_store.pandas import GPTPandasIndex, PandasIndex
from llama_index_spanish.indices.struct_store.sql import (
    GPTSQLStructStoreIndex,
    SQLStructStoreIndex,
)
from llama_index_spanish.indices.tree.base import GPTTreeIndex, TreeIndex
from llama_index_spanish.indices.vector_store import GPTVectorStoreIndex, VectorStoreIndex

__all__ = [
    "load_graph_from_storage",
    "load_index_from_storage",
    "load_indices_from_storage",
    "KeywordTableIndex",
    "SimpleKeywordTableIndex",
    "RAKEKeywordTableIndex",
    "SummaryIndex",
    "TreeIndex",
    "VectaraIndex",
    "DocumentSummaryIndex",
    "KnowledgeGraphIndex",
    "PandasIndex",
    "VectorStoreIndex",
    "SQLStructStoreIndex",
    "MultiModalVectorStoreIndex",
    "EmptyIndex",
    "ComposableGraph",
    # legacy
    "GPTKnowledgeGraphIndex",
    "GPTKeywordTableIndex",
    "GPTSimpleKeywordTableIndex",
    "GPTRAKEKeywordTableIndex",
    "GPTDocumentSummaryIndex",
    "GPTListIndex",
    "GPTTreeIndex",
    "GPTPandasIndex",
    "ListIndex",
    "GPTVectorStoreIndex",
    "GPTSQLStructStoreIndex",
    "GPTEmptyIndex",
]
