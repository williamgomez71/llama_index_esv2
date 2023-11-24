try:
    from guidance.llms import Mock as MockLLM
except ImportError:
    MockLLM = None  # type: ignore
import pytest
from llama_index_spanish.question_gen.guidance_generator import GuidanceQuestionGenerator
from llama_index_spanish.question_gen.types import SubQuestion
from llama_index_spanish.schema import QueryBundle
from llama_index_spanish.tools.types import ToolMetadata


@pytest.mark.skipif(MockLLM is None, reason="guidance not installed")
def test_guidance_question_generator() -> None:
    question_gen = GuidanceQuestionGenerator.from_defaults(guidance_llm=MockLLM())

    tools = [
        ToolMetadata(name="test_tool_1", description="test_description_1"),
        ToolMetadata(name="test_tool_2", description="test_description_2"),
    ]
    output = question_gen.generate(tools=tools, query=QueryBundle("test query"))
    assert isinstance(output[0], SubQuestion)
