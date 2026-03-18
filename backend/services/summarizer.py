from services.llm import get_llm
from services.prompts import chunk_prompt, final_prompt

llm = get_llm()


def summarize_chunk(chunk: str) -> str:
    """
    Summarize a single transcript chunk using LCEL (prompt | llm).
    
    Args:
        chunk: A text chunk from the transcript.
    
    Returns:
        Summarized text for this chunk.
    """
    chain = chunk_prompt | llm
    return chain.invoke({"input": chunk}).content


def summarize_all(chunks: list[str]) -> str:
    """
    Map-Reduce style summarization:
    1. Map: Summarize each chunk individually.
    2. Reduce: Combine all summaries into a final blog article.
    
    Args:
        chunks: List of text chunks.
    
    Returns:
        A well-structured blog article.
    """
    # Map — summarize each chunk
    summaries = [summarize_chunk(c) for c in chunks]

    # Reduce — combine into final article
    combined = "\n\n".join(summaries)
    final_chain = final_prompt | llm
    result = final_chain.invoke({"input": combined})

    return result.content
