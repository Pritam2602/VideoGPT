from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, MODEL


def get_llm(streaming: bool = False) -> ChatGoogleGenerativeAI:
    """
    Returns a ChatGoogleGenerativeAI (Gemini) instance.
    
    Args:
        streaming: Enable streaming for real-time token output.
    
    Returns:
        A configured Gemini LLM instance.
    """
    return ChatGoogleGenerativeAI(
        model=MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
        streaming=streaming,
    )
