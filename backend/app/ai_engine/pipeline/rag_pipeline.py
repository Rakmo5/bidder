from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.ai_engine.config import ai_config
from app.ai_engine.chunking.base_chunker import DocumentChunk
from app.ai_engine.chunking.layout_aware_chunker import LayoutAwarePDFChunker
from app.ai_engine.vector_store.base_store import RetrievalResult
from app.ai_engine.vector_store.bm25_retriever import InMemoryBM25HybridStore
from app.ai_engine.llm_providers.groq_provider import GroqLLMProvider
from app.ai_engine.llm_providers.gemini_provider import GeminiLLMProvider
from app.ai_engine.llm_providers.fallback_provider import DeterministicFallbackProvider
from app.core.config import settings

class RAGAnswer(BaseModel):
    query: str
    target_document: str
    answer: str
    grounded_evidence: str
    page_number: int
    normalized_bbox: List[float]
    confidence_score: float
    retrieved_chunks: List[RetrievalResult]
    llm_provider_used: str

class RAGPipeline:
    """
    Modular Retrieval-Augmented Generation (RAG) Orchestrator.
    Combines Document Chunking, Hybrid BM25/Semantic Indexing, and Grounded Multi-LLM Synthesis.
    """

    def __init__(self):
        self.chunker = LayoutAwarePDFChunker()
        self.vector_store = InMemoryBM25HybridStore()
        self.groq_provider = GroqLLMProvider()
        self.gemini_provider = GeminiLLMProvider()
        self.fallback_provider = DeterministicFallbackProvider()

    def index_document(self, file_path: Path) -> List[DocumentChunk]:
        """Chunks and stores a PDF document in the hybrid vector store."""
        chunks = self.chunker.chunk_file(file_path)
        if chunks:
            self.vector_store.add_chunks(file_path.name, chunks)
        return chunks

    def retrieve(self, document_name: str, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """Retrieves top-k relevant chunks, auto-indexing the file if not already present."""
        chunks = self.vector_store.get_chunks(document_name)
        if not chunks:
            # Auto-index from demo_pdfs or uploads
            possible_dirs = [
                Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "demo_pdfs",
                Path(__file__).resolve().parent.parent.parent.parent / "data" / "demo_pdfs",
                settings.UPLOAD_DIR
            ]
            for d in possible_dirs:
                candidate = d / document_name
                if candidate.exists():
                    self.index_document(candidate)
                    break

        return self.vector_store.search(document_name, query, top_k=top_k)

    def query(self, document_name: str, user_query: str) -> RAGAnswer:
        """Executes full RAG query: Retrieval -> Context Assembly -> LLM Grounding."""
        retrieved = self.retrieve(document_name, user_query, top_k=ai_config.top_k_retrieval)

        if not retrieved:
            return RAGAnswer(
                query=user_query,
                target_document=document_name,
                answer=f"No indexed evidence chunks found for document '{document_name}'.",
                grounded_evidence="N/A",
                page_number=1,
                normalized_bbox=[10.0, 30.0, 80.0, 15.0],
                confidence_score=0.0,
                retrieved_chunks=[],
                llm_provider_used="none"
            )

        top_chunk = retrieved[0].chunk
        context_str = "\n\n".join([f"[Page {r.chunk.page_number}]: {r.chunk.text}" for r in retrieved])
        user_prompt = f"AUDIT QUESTION: {user_query}\n\nRETRIEVED DOCUMENT CONTEXT:\n{context_str}"

        # 1. Try Groq
        if self.groq_provider.is_available():
            result = self.groq_provider.generate_json(ai_config.rag_system_prompt, user_prompt)
            if result and "answer" in result:
                return RAGAnswer(
                    query=user_query,
                    target_document=document_name,
                    answer=result["answer"],
                    grounded_evidence=result.get("grounded_evidence", top_chunk.text),
                    page_number=top_chunk.page_number,
                    normalized_bbox=top_chunk.normalized_bbox,
                    confidence_score=float(result.get("confidence_score", 0.95)),
                    retrieved_chunks=retrieved,
                    llm_provider_used=f"Groq ({ai_config.groq_primary_model})"
                )

        # 2. Try Gemini
        if self.gemini_provider.is_available():
            result = self.gemini_provider.generate_json(ai_config.rag_system_prompt, user_prompt)
            if result and "answer" in result:
                return RAGAnswer(
                    query=user_query,
                    target_document=document_name,
                    answer=result["answer"],
                    grounded_evidence=result.get("grounded_evidence", top_chunk.text),
                    page_number=top_chunk.page_number,
                    normalized_bbox=top_chunk.normalized_bbox,
                    confidence_score=float(result.get("confidence_score", 0.95)),
                    retrieved_chunks=retrieved,
                    llm_provider_used=f"Google Gemini ({ai_config.gemini_primary_model})"
                )

        # 3. Deterministic Grounded Synthesis Fallback
        return RAGAnswer(
            query=user_query,
            target_document=document_name,
            answer=f"Verified finding from Page {top_chunk.page_number}: {top_chunk.text}",
            grounded_evidence=top_chunk.text[:200],
            page_number=top_chunk.page_number,
            normalized_bbox=top_chunk.normalized_bbox,
            confidence_score=0.90,
            retrieved_chunks=retrieved,
            llm_provider_used="Deterministic Hybrid RAG Matcher"
        )
