from typing import List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    top_k: int = 4


class Source(BaseModel):
    file_name: str
    content: str
    score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
