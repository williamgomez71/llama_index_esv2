"""Init file."""

from llama_index_spanish.embeddings.adapter import (
    AdapterEmbeddingModel,
    LinearAdapterEmbeddingModel,
)
from llama_index_spanish.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index_spanish.embeddings.base import BaseEmbedding, SimilarityMode
from llama_index_spanish.embeddings.bedrock import BedrockEmbedding
from llama_index_spanish.embeddings.clarifai import ClarifaiEmbedding
from llama_index_spanish.embeddings.clip import ClipEmbedding
from llama_index_spanish.embeddings.cohereai import CohereEmbedding
from llama_index_spanish.embeddings.elasticsearch import (
    ElasticsearchEmbedding,
    ElasticsearchEmbeddings,
)
from llama_index_spanish.embeddings.fastembed import FastEmbedEmbedding
from llama_index_spanish.embeddings.google import GoogleUnivSentEncoderEmbedding
from llama_index_spanish.embeddings.google_palm import GooglePaLMEmbedding
from llama_index_spanish.embeddings.gradient import GradientEmbedding
from llama_index_spanish.embeddings.huggingface import (
    HuggingFaceEmbedding,
    HuggingFaceInferenceAPIEmbedding,
    HuggingFaceInferenceAPIEmbeddings,
)
from llama_index_spanish.embeddings.huggingface_optimum import OptimumEmbedding
from llama_index_spanish.embeddings.huggingface_utils import DEFAULT_HUGGINGFACE_EMBEDDING_MODEL
from llama_index_spanish.embeddings.instructor import InstructorEmbedding
from llama_index_spanish.embeddings.langchain import LangchainEmbedding
from llama_index_spanish.embeddings.llm_rails import LLMRailsEmbedding, LLMRailsEmbeddings
from llama_index_spanish.embeddings.openai import OpenAIEmbedding
from llama_index_spanish.embeddings.pooling import Pooling
from llama_index_spanish.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index_spanish.embeddings.utils import resolve_embed_model
from llama_index_spanish.embeddings.voyageai import VoyageEmbedding

__all__ = [
    "AdapterEmbeddingModel",
    "BedrockEmbedding",
    "ClarifaiEmbedding",
    "ClipEmbedding",
    "CohereEmbedding",
    "BaseEmbedding",
    "DEFAULT_HUGGINGFACE_EMBEDDING_MODEL",
    "ElasticsearchEmbedding",
    "FastEmbedEmbedding",
    "GoogleUnivSentEncoderEmbedding",
    "GradientEmbedding",
    "HuggingFaceInferenceAPIEmbedding",
    "HuggingFaceEmbedding",
    "InstructorEmbedding",
    "LangchainEmbedding",
    "LinearAdapterEmbeddingModel",
    "LLMRailsEmbedding",
    "OpenAIEmbedding",
    "AzureOpenAIEmbedding",
    "OptimumEmbedding",
    "Pooling",
    "GooglePaLMEmbedding",
    "SimilarityMode",
    "TextEmbeddingsInference",
    "resolve_embed_model",
    # Deprecated, kept for backwards compatibility
    "LLMRailsEmbeddings",
    "ElasticsearchEmbeddings",
    "HuggingFaceInferenceAPIEmbeddings",
    "VoyageEmbedding",
]
