from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.summarize import router as summarize_router

app = FastAPI(
    title="VideoGPT API",
    description="Universal Video → Article Generator powered by LangChain & Gemini",
    version="1.0.0",
)

# CORS — allow the React frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(summarize_router)


@app.get("/")
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok", "message": "VideoGPT API is running 🚀"}
