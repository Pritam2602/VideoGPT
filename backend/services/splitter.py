from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(text: str, chunk_size: int = 2000, chunk_overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks using LangChain's RecursiveCharacterTextSplitter.
    
    Better than naive word splitting — handles token boundaries properly.
    
    Args:
        text: The full transcript text.
        chunk_size: Max characters per chunk.
        chunk_overlap: Overlap between chunks for context continuity.
    
    Returns:
        A list of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)
