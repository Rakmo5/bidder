from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel
from app.ai_engine.chunking.base_chunker import DocumentChunk

class RetrievalResult(BaseModel):
    chunk: DocumentChunk
    similarity_score: float
    retrieval_mode: str

class BaseVectorStore(ABC):
    """Abstract Base Class for Vector & Hybrid Document Storage."""

    @abstractmethod
    def add_chunks(self, document_name: str, chunks: List[DocumentChunk]):
        """Indexes document chunks into the store."""
        pass

    @abstractmethod
    def search(self, document_name: str, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """Retrieves the top-k most relevant chunks for a query."""
        pass
