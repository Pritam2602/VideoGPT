from services.extractor import download_audio
from services.transcript import generate_transcript
from services.smart_pipeline import smart_summarizer


def generate_article(video_url: str) -> str:
    """
    End-to-end pipeline: Video URL → Blog Article.
    
    1. Download audio from the video.
    2. Transcribe audio using Whisper.
    3. Smart summarize (auto-selects direct vs map-reduce based on length).
    
    Args:
        video_url: URL of the video (YouTube, Vimeo, etc.)
    
    Returns:
        A well-structured blog article as a string.
    """
    # Step 1: Extract audio
    audio_path = download_audio(video_url)

    # Step 2: Transcribe
    transcript = generate_transcript(audio_path)

    # Step 3: Smart summarization (RunnableBranch handles routing)
    article = smart_summarizer.invoke(transcript)

    return article
