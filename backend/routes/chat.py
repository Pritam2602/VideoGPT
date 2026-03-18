from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from services.rag_pipeline import get_rag_chain

router = APIRouter()


def _extract_text(chunk):
    """Convert chunk into safe string for streaming."""

    # Step 1: get content
    if hasattr(chunk, "content"):
        content = chunk.content
    else:
        content = chunk

    # Step 2: handle list (your main error)
    if isinstance(content, list):
        return " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    # Step 3: handle dict
    if isinstance(content, dict):
        return content.get("text", str(content))

    # Step 4: fallback
    return str(content)


def _stream_generator(query: str, video_id: str = None):
    """Yield streaming chunks from the RAG chain."""
    chain = get_rag_chain(video_id)

    for chunk in chain.stream(query):
        text = _extract_text(chunk)

        if text:   # avoid empty chunks
            yield text


@router.get("/chat")
async def chat(
    query: str = Query(..., description="The question to ask about the video"),
    video_id: str = Query(None, description="Optional video ID to filter context"),
):
    """
    Chat with video content using RAG.
    
    Streams the response in real-time as the LLM generates tokens.
    """
    return StreamingResponse(
        _stream_generator(query, video_id),
        media_type="text/plain",
    )
