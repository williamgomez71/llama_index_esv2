"""Test tools."""
import pytest
from llama_index_spanish.bridge.pydantic import BaseModel
from llama_index_spanish.tools.function_tool import FunctionTool

try:
    import langchain
except ImportError:
    langchain = None  # type: ignore


def tmp_function(x: int) -> str:
    return str(x)


async def async_tmp_function(x: int) -> str:
    return "async_" + str(x)


def test_function_tool() -> None:
    """Test function tool."""
    function_tool = FunctionTool.from_defaults(
        lambda x: str(x), name="foo", description="bar"
    )
    assert function_tool.metadata.name == "foo"
    assert function_tool.metadata.description == "bar"
    assert function_tool.metadata.fn_schema is not None
    actual_schema = function_tool.metadata.fn_schema.schema()
    # note: no type
    assert "x" in actual_schema["properties"]

    result = function_tool(1)
    assert str(result) == "1"

    # test adding typing to function

    function_tool = FunctionTool.from_defaults(
        tmp_function, name="foo", description="bar"
    )
    assert function_tool.metadata.fn_schema is not None
    actual_schema = function_tool.metadata.fn_schema.schema()
    assert actual_schema["properties"]["x"]["type"] == "integer"


@pytest.mark.skipif(langchain is None, reason="langchain not installed")
def test_function_tool_to_langchain() -> None:
    function_tool = FunctionTool.from_defaults(
        tmp_function, name="foo", description="bar"
    )

    # test to langchain
    # NOTE: can't take in a function with int args
    langchain_tool = function_tool.to_langchain_tool()
    result = langchain_tool.run("1")
    assert result == "1"

    # test langchain structured tool
    class TestSchema(BaseModel):
        x: int
        y: int

    function_tool = FunctionTool.from_defaults(
        lambda x, y: str(x) + "," + str(y),
        name="foo",
        description="bar",
        fn_schema=TestSchema,
    )
    assert str(function_tool(1, 2)) == "1,2"
    langchain_tool2 = function_tool.to_langchain_structured_tool()
    assert langchain_tool2.run({"x": 1, "y": 2}) == "1,2"
    assert langchain_tool2.args_schema == TestSchema


@pytest.mark.asyncio()
async def test_function_tool_async() -> None:
    """Test function tool async."""
    function_tool = FunctionTool.from_defaults(
        fn=tmp_function, async_fn=async_tmp_function, name="foo", description="bar"
    )
    assert function_tool.metadata.fn_schema is not None
    actual_schema = function_tool.metadata.fn_schema.schema()
    assert actual_schema["properties"]["x"]["type"] == "integer"

    assert str(function_tool(2)) == "2"
    assert str(await function_tool.acall(2)) == "async_2"


@pytest.mark.skipif(langchain is None, reason="langchain not installed")
@pytest.mark.asyncio()
async def test_function_tool_async_langchain() -> None:
    function_tool = FunctionTool.from_defaults(
        fn=tmp_function, async_fn=async_tmp_function, name="foo", description="bar"
    )

    # test to langchain
    # NOTE: can't take in a function with int args
    langchain_tool = function_tool.to_langchain_tool()
    result = await langchain_tool.arun("1")
    assert result == "async_1"

    # test langchain structured tool
    class TestSchema(BaseModel):
        x: int
        y: int

    def structured_tmp_function(x: int, y: int) -> str:
        return str(x) + "," + str(y)

    async def async_structured_tmp_function(x: int, y: int) -> str:
        return "async_" + str(x) + "," + str(y)

    function_tool = FunctionTool.from_defaults(
        fn=structured_tmp_function,
        async_fn=async_structured_tmp_function,
        name="foo",
        description="bar",
        fn_schema=TestSchema,
    )
    assert str(await function_tool.acall(1, 2)) == "async_1,2"
    langchain_tool2 = function_tool.to_langchain_structured_tool()
    assert (await langchain_tool2.arun({"x": 1, "y": 2})) == "async_1,2"
    assert langchain_tool2.args_schema == TestSchema


@pytest.mark.asyncio()
async def test_function_tool_async_defaults() -> None:
    """Test async calls to function tool when only sync function is given."""
    function_tool = FunctionTool.from_defaults(
        fn=tmp_function, name="foo", description="bar"
    )
    assert function_tool.metadata.fn_schema is not None
    actual_schema = function_tool.metadata.fn_schema.schema()
    assert actual_schema["properties"]["x"]["type"] == "integer"


@pytest.mark.skipif(langchain is None, reason="langchain not installed")
@pytest.mark.asyncio()
async def test_function_tool_async_defaults_langchain() -> None:
    function_tool = FunctionTool.from_defaults(
        fn=tmp_function, name="foo", description="bar"
    )

    # test to langchain
    # NOTE: can't take in a function with int args
    langchain_tool = function_tool.to_langchain_tool()
    result = await langchain_tool.arun("1")
    assert result == "1"


from llama_index_spanish import (
    ServiceContext,
    VectorStoreIndex,
)
from llama_index_spanish.schema import Document
from llama_index_spanish.token_counter.mock_embed_model import MockEmbedding
from llama_index_spanish.tools import RetrieverTool, ToolMetadata


def test_retreiver_tool() -> None:
    doc1 = Document(
        text=("# title1:Hello world.\n" "This is a test.\n"),
        metadata={"file_path": "/data/personal/essay.md"},
    )

    doc2 = Document(
        text=("# title2:This is another test.\n" "This is a test v2."),
        metadata={"file_path": "/data/personal/essay.md"},
    )
    service_context = ServiceContext.from_defaults(
        llm=None, embed_model=MockEmbedding(embed_dim=1)
    )
    vs_index = VectorStoreIndex.from_documents(
        [doc1, doc2], service_context=service_context
    )
    vs_retriever = vs_index.as_retriever()
    vs_ret_tool = RetrieverTool(
        retriever=vs_retriever,
        metadata=ToolMetadata(
            name="knowledgebase",
            description="test",
        ),
    )
    output = vs_ret_tool.call("arg1", "arg2", key1="v1", key2="v2")
    formated_doc = (
        "file_path = /data/personal/essay.md\n"
        "# title1:Hello world.\n"
        "This is a test."
    )
    assert formated_doc in output.content
