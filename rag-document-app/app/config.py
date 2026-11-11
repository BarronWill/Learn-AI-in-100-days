from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "document-rag-app"
    chunk_size: int = 500
    chunk_overlap: int = 100
    chunk_strategy: str = "recursive"  # "fixed" | "recursive"
    top_k: int = 4
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "gpt-4o-mini"
    vector_store_collection: str = "documents"


settings = Settings()
