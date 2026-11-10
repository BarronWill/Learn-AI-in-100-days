"""Document RAG application package."""
from services.document_service import extract_text_from_file, process_document

file = extract_text_from_file("file/test.txt")
chunk_text = process_document("file/test.txt")
pass