from llama_index_spanish.storage.docstore.firestore_docstore import FirestoreDocumentStore
from llama_index_spanish.storage.docstore.keyval_docstore import KVDocumentStore
from llama_index_spanish.storage.docstore.mongo_docstore import MongoDocumentStore
from llama_index_spanish.storage.docstore.redis_docstore import RedisDocumentStore

# alias for backwards compatibility
from llama_index_spanish.storage.docstore.simple_docstore import (
    DocumentStore,
    SimpleDocumentStore,
)
from llama_index_spanish.storage.docstore.types import BaseDocumentStore

__all__ = [
    "BaseDocumentStore",
    "DocumentStore",
    "FirestoreDocumentStore",
    "SimpleDocumentStore",
    "MongoDocumentStore",
    "KVDocumentStore",
    "RedisDocumentStore",
]
