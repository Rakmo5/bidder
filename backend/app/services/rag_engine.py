from pathlib import Path
from typing import List, Dict, Any, Optional
from app.ai_engine.chunking.base_chunker import DocumentChunk
from app.ai_engine.vector_store.base_store import RetrievalResult
from app.ai_engine.pipeline.rag_pipeline import RAGPipeline, RAGAnswer

# Initialize global modular RAG pipeline
rag_engine_instance = RAGPipeline()

class HybridRAGEngine:
    """Service facade exposing modular AI Engine capabilities to API layer."""
    
    def __init__(self):
        self._pipeline = rag_engine_instance

    @property
    def vector_store(self) -> Dict[str, List[DocumentChunk]]:
        return self._pipeline.vector_store._store

    def index_pdf_document(self, file_path: Path) -> List[DocumentChunk]:
        return self._pipeline.index_document(file_path)

    def retrieve_relevant_chunks(self, doc_name: str, query: str, top_k: int = 3) -> List[RetrievalResult]:
        return self._pipeline.retrieve(doc_name, query, top_k=top_k)

    def query_rag(self, doc_name: str, user_query: str) -> RAGAnswer:
        return self._pipeline.query(doc_name, user_query)

rag_pipeline = HybridRAGEngine()
