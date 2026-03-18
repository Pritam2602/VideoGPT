from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config import GOOGLE_API_KEY

# Embedding model for vector similarity search
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

# In-memory vector store (persists for the lifetime of the server)
vector_db = None


def create_vector_store(chunks: list[str], video_id: str):
    """
    Create a new FAISS vector store from text chunks, or add to existing one.
    
    Each chunk is tagged with a video_id in metadata so we can
    filter retrieval per video or search across all videos.
    
    Args:
        chunks: List of text chunks from a transcript.
        video_id: Unique identifier for the video (e.g., YouTube video ID).
    """
    global vector_db

    docs = [
        Document(page_content=chunk, metadata={"video_id": video_id})
        for chunk in chunks
    ]

    if vector_db is None:
        vector_db = FAISS.from_documents(docs, embedding)
    else:
        vector_db.add_documents(docs)


def get_retriever(video_id: str = None):
    """
    Get a retriever from the vector store.
    
    Args:
        video_id: If provided, only retrieve chunks from this specific video.
                  If None, search across all indexed videos.
    
    Returns:
        A LangChain retriever instance.
    
    Raises:
        ValueError: If no videos have been indexed yet.
    """
    if vector_db is None:
        raise ValueError("No videos have been indexed yet. Process a video first.")

    if video_id:
        return vector_db.as_retriever(
            search_kwargs={"k": 4, "filter": {"video_id": video_id}}
        )
    return vector_db.as_retriever(search_kwargs={"k": 4})
