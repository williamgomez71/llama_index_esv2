from llama_index_spanish.embeddings import OpenAIEmbedding
from llama_index_spanish.extractors import KeywordExtractor
from llama_index_spanish.ingestion.pipeline import IngestionPipeline
from llama_index_spanish.llms import MockLLM
from llama_index_spanish.node_parser import SentenceSplitter
from llama_index_spanish.readers import ReaderConfig, StringIterableReader
from llama_index_spanish.schema import Document


def test_build_pipeline() -> None:
    pipeline = IngestionPipeline(
        reader=ReaderConfig(
            reader=StringIterableReader(), reader_kwargs={"texts": ["This is a test."]}
        ),
        documents=[Document.example()],
        transformations=[
            SentenceSplitter(),
            KeywordExtractor(llm=MockLLM()),
            OpenAIEmbedding(api_key="fake"),
        ],
    )

    assert len(pipeline.transformations) == 3


def test_run_pipeline() -> None:
    pipeline = IngestionPipeline(
        reader=ReaderConfig(
            reader=StringIterableReader(), reader_kwargs={"texts": ["This is a test."]}
        ),
        documents=[Document.example()],
        transformations=[
            SentenceSplitter(),
            KeywordExtractor(llm=MockLLM()),
        ],
    )

    nodes = pipeline.run()

    assert len(nodes) == 2
    assert len(nodes[0].metadata) > 0
