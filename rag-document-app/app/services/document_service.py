from pathlib import Path
from typing import List

from config import settings
from core.chunking import split_text_into_chunks
from schemas.document import DocumentChunk, DocumentMetadata


def extract_text_from_file(file_path: str) -> str:
    """Read text from PDF, TXT, DOCX files."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        # utf-8-sig strips the BOM that Notepad often adds; "replace" keeps broken bytes visible
        return path.read_text(encoding="utf-8-sig", errors="replace")

    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages)

    if suffix == ".docx":
        from docx import Document

        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    raise ValueError(f"Unsupported file type: {suffix}")


def process_document(file_path: str) -> List[DocumentChunk]:
    """Extract text, chunk it, build DocumentChunk objects."""
    path = Path(file_path)
    text = extract_text_from_file(file_path)
    if not text.strip():
        raise ValueError(f"No text could be extracted from {path.name} (scanned PDF?)")

    chunks = split_text_into_chunks(
        text,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    file_name = path.name
    file_type = path.suffix.lower().lstrip(".")
    document_chunks: List[DocumentChunk] = []

    for index, chunk in enumerate(chunks):
        document_chunks.append(
            DocumentChunk(
                id=f"{file_name}_{index}",
                text=chunk,
                metadata=DocumentMetadata(
                    file_name=file_name,
                    file_type=file_type,
                    source_path=file_path,
                ),
            )
        )

    return document_chunks
