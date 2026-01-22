"""
Vector Store - ChromaDB Management
Learn: How to store and retrieve vector embeddings
"""
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from services.embeddings import get_embeddings_model
import logging
import os

logger = logging.getLogger(__name__)


def setup_vector_store(
    documents: List[Document],
    persist_directory: str = "./chroma_db",
    collection_name: str = "github_rag"
) -> Chroma:
    """
    LEARN: Vector stores convert text → numbers (embeddings) → searchable database
    
    Why ChromaDB?
    - Persistent (saves to disk)
    - Fast similarity search
    - No server needed (embedded)
    
    Args:
        documents: Chunks from document_processor
        persist_directory: Where to save on disk
        collection_name: Database "table" name
    
    Returns:
        Searchable vector database
    """
    logger.info("💾 Creating Vector Store...")
    logger.info(f"   Directory: {persist_directory}")
    logger.info(f"   Documents: {len(documents)}")
    
    # Step 1: Get embedding model (converts text → vectors)
    embeddings = get_embeddings_model()
    
    # Step 2: Create vector store
    # This does:
    # - For each document → create embedding (384-dim vector)
    # - Store in ChromaDB
    # - Save to disk
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    
    count = vectorstore._collection.count()
    logger.info(f"✅ Vector store ready with {count} documents")
    
    return vectorstore


def load_vector_store(
    persist_directory: str = "./chroma_db",
    collection_name: str = "github_rag"
) -> Optional[Chroma]:
    """
    LEARN: Load existing database (no re-embedding needed)
    
    Why this matters: Re-embedding is slow. Load from disk when restarting app.
    """
    if not os.path.exists(persist_directory):
        logger.warning(f"⚠️  No database found at {persist_directory}")
        return None
    
    logger.info(f"📂 Loading vector store from disk...")
    
    embeddings = get_embeddings_model()
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    count = vectorstore._collection.count()
    logger.info(f"✅ Loaded {count} documents")
    
    return vectorstore