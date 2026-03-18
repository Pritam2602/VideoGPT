from langchain.schema.runnable import RunnableLambda, RunnableBranch
from services.splitter import split_text
from services.summarizer import summarize_all
from services.llm import get_llm
from services.prompts import final_prompt

llm = get_llm()


def _is_long(text: str) -> bool:
    """Check if text is too long for a single LLM call (>3000 words)."""
    return len(text.split()) > 3000


def _short_summary(text: str) -> str:
    """Directly summarize short text in one LLM call."""
    chain = final_prompt | llm
    return chain.invoke({"input": text}).content


def _long_summary(text: str) -> str:
    """Chunk and map-reduce summarize long text."""
    chunks = split_text(text)
    return summarize_all(chunks)


# RunnableBranch: dynamically routes based on text length
# - Long text  → chunk + map-reduce
# - Short text → direct summary
smart_summarizer = RunnableBranch(
    (lambda x: _is_long(x), RunnableLambda(_long_summary)),
    RunnableLambda(_short_summary),  # default fallback
)
