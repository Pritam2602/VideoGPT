from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.article_generator import generate_article

router = APIRouter()


class SummarizeRequest(BaseModel):
    """Request body for the /summarize endpoint."""
    url: str


class SummarizeResponse(BaseModel):
    """Response body for the /summarize endpoint."""
    article: str


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_video(data: SummarizeRequest):
    """
    Generate a blog article from a video URL.
    
    Accepts any video link (YouTube, Vimeo, etc.) and returns
    a well-structured article generated via the LangChain pipeline.
    """
    try:
        article = generate_article(data.url)
        return SummarizeResponse(article=article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
