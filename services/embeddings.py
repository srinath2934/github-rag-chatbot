"""
Embeddings - Convert text to vectors using HuggingFace
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

def get_embeddings_model():
    """
    Initialize and return the embeddings model.
    
    Uses sentence-transformers/all-MiniLM-L6-v2:
    - Fast and lightweight
    - Good for code and documentation
    - 384-dimensional vectors
    
    Returns:
        HuggingFaceEmbeddings model instance
    """
    logger.info("🧠 Loading embeddings model (all-MiniLM-L6-v2)...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Using CPU (change to 'cuda' if you have GPU)
        encode_kwargs={'normalize_embeddings': True}
    )
    
    logger.info("✅ Embeddings model loaded and ready")
    return embeddings


# Test function
if __name__ == "__main__":
    # Quick test
    embeddings = get_embeddings_model()
    
    # Test embedding
    sample_text = "def hello(): print('Hello, world!')"
    vector = embeddings.embed_query(sample_text)
    
    print(f"Sample text: {sample_text}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
