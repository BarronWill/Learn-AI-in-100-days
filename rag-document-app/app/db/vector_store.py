from typing import List


class VectorStore:
    """Wrapper around ChromaDB or Qdrant."""

    def __init__(self):
        # TODO: initialize collection / client
        pass

    def add_documents(self, chunks: List[str], metadata: List[dict]):
        """Store chunks and their metadata in vector DB."""
        # TODO: create embeddings and persist documents
        pass

    def similarity_search(self, query: str, top_k: int = 4):
        """Return top-k relevant documents for a query."""
        # TODO: embed query and search vector store
        return []
