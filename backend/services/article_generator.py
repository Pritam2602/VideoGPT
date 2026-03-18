import re
from services.extractor import download_audio
from services.transcript import generate_transcript
from services.smart_pipeline import smart_summarizer
from services.splitter import split_text
from services.vector_store import create_vector_store


def _extract_video_id(url: str) -> str:
    """Extract a video ID from a URL for metadata tagging."""
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    return match.group(1) if match else url.split("/")[-1][:20]

def extract_text(result):
    """Convert LangChain/LLM output into plain string."""
    
    # Case 1: AIMessage
    if hasattr(result, "content"):
        return result.content

    # Case 2: list of dicts (your current error)
    if isinstance(result, list):
        return " ".join(
            r.get("text", "") if isinstance(r, dict) else str(r)
            for r in result
        )

    # Case 3: dict
    if isinstance(result, dict):
        return result.get("text", str(result))

    # Fallback
    return str(result)

def generate_article(video_url: str) -> tuple[str, str]:
    """
    End-to-end pipeline: Video URL → Blog Article.
    
    1. Download audio from the video.
    2. Transcribe audio using Whisper.
    3. Split transcript & index into vector store (for RAG chat).
    4. Smart summarize (auto-selects direct vs map-reduce based on length).
    
    Args:
        video_url: URL of the video (YouTube, Vimeo, etc.)
    
    Returns:
        A tuple of (article, video_id).
    """
    video_id = _extract_video_id(video_url)

    # Step 1: Extract audio
    audio_path = download_audio(video_url)

    # Step 2: Transcribe
    transcript = generate_transcript(audio_path)

    # Step 3: Index into vector store for RAG chat
    chunks = split_text(transcript)
    create_vector_store(chunks, video_id)

    # Step 4: Smart summarization (RunnableBranch handles routing)
    result = smart_summarizer.invoke(transcript)
    article = extract_text(result)

    return article, video_id
