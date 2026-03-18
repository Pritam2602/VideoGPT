from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from services.vector_store import get_retriever
from services.llm import get_llm

# RAG prompt — answers questions based on retrieved context
rag_prompt = ChatPromptTemplate.from_template(
    """You are an intelligent assistant that answers questions about video content.

Use ONLY the following context from the video transcript to answer the question.
If the context doesn't contain enough information, say so honestly.

## Context
{context}

## Question
{question}

## Answer"""
)


def _format_docs(docs) -> str:
    """Format retrieved documents into a single string."""
    return "\n\n".join([doc.page_content for doc in docs])


def get_rag_chain(video_id: str = None):
    """
    Build a RAG chain with streaming support.
    
    Pipeline: question → retriever → format docs → prompt → LLM (streaming)
    
    Args:
        video_id: Optional video ID to filter retrieval to a specific video.
    
    Returns:
        An LCEL chain that streams responses.
    """
    retriever = get_retriever(video_id)
    llm = get_llm(streaming=True)

    chain = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | rag_prompt
        | llm
    )

    return chain
