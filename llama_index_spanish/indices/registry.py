"""Index registry."""

from typing import Dict, Type

from llama_index_spanish.data_structs.struct_type import IndexStructType
from llama_index_spanish.indices.base import BaseIndex
from llama_index_spanish.indices.document_summary.base import DocumentSummaryIndex
from llama_index_spanish.indices.empty.base import EmptyIndex
from llama_index_spanish.indices.keyword_table.base import KeywordTableIndex
from llama_index_spanish.indices.knowledge_graph.base import KnowledgeGraphIndex
from llama_index_spanish.indices.list.base import SummaryIndex
from llama_index_spanish.indices.multi_modal import MultiModalVectorStoreIndex
from llama_index_spanish.indices.struct_store.pandas import PandasIndex
from llama_index_spanish.indices.struct_store.sql import SQLStructStoreIndex
from llama_index_spanish.indices.tree.base import TreeIndex
from llama_index_spanish.indices.vector_store.base import VectorStoreIndex

INDEX_STRUCT_TYPE_TO_INDEX_CLASS: Dict[IndexStructType, Type[BaseIndex]] = {
    IndexStructType.TREE: TreeIndex,
    IndexStructType.LIST: SummaryIndex,
    IndexStructType.KEYWORD_TABLE: KeywordTableIndex,
    IndexStructType.VECTOR_STORE: VectorStoreIndex,
    IndexStructType.SQL: SQLStructStoreIndex,
    IndexStructType.PANDAS: PandasIndex,
    IndexStructType.KG: KnowledgeGraphIndex,
    IndexStructType.EMPTY: EmptyIndex,
    IndexStructType.DOCUMENT_SUMMARY: DocumentSummaryIndex,
    IndexStructType.MULTIMODAL_VECTOR_STORE: MultiModalVectorStoreIndex,
}
