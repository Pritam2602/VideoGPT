import whisper

# Load model once at module level for reuse
_model = None


def _get_model(model_size: str = "base"):
    """Lazy-load the Whisper model."""
    global _model
    if _model is None:
        _model = whisper.load_model(model_size)
    return _model


def generate_transcript(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe an audio file using OpenAI Whisper (local).
    
    Args:
        audio_path: Path to the audio file.
        model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large').
    
    Returns:
        The full transcript as a string.
    """
    model = _get_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]
