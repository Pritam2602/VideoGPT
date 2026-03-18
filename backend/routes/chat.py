from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from services.rag_pipeline import get_rag_chain

router = APIRouter()


def _stream_generator(query: str, video_id: str = None):
    """Yield streaming chunks from the RAG chain."""
    chain = get_rag_chain(video_id)
    for chunk in chain.stream(query):
        if hasattr(chunk, "content"):
            yield chunk.content
        else:
            yield str(chunk)


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
