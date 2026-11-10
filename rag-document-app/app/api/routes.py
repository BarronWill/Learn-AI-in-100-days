from fastapi import APIRouter, File, UploadFile

from schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["document-rag"])


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and index it into the vector store."""
    # TODO: validate file type, extract text, chunk, embed, store
    return {"message": "Document uploaded successfully"}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_documents(request: ChatRequest):
    """Answer a question using the indexed documents."""
    # TODO: retrieve relevant chunks, build prompt, call LLM, return answer
    return ChatResponse(answer="", sources=[])
