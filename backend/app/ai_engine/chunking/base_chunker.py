from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    text: str
    normalized_bbox: List[float] # [x, y, w, h] in percentages
    tokens_count: int

class BaseChunker(ABC):
    """Abstract Base Class defining the document chunking contract."""
    
    @abstractmethod
    def chunk_file(self, file_path: Path) -> List[DocumentChunk]:
        """Splits a document file into discrete, metadata-annotated DocumentChunks."""
        pass
