from pydantic import BaseModel
from typing import Optional


class DocumentMetadata(BaseModel):
    file_name: str
    file_type: str
    source_path: Optional[str] = None
    page_number: Optional[int] = None


class DocumentChunk(BaseModel):
    id: str
    text: str
    metadata: DocumentMetadata
