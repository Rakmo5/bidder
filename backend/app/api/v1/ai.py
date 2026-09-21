from typing import List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from app.core.config import settings
from app.services.rag_engine import rag_pipeline, RAGAnswer, DocumentChunk

router = APIRouter()

class RAGQueryRequest(BaseModel):
    document_name: str
    query: str
    top_k: int = 3

@router.get("/status")
async def get_rag_pipeline_status():
    """Returns the live health, vector store stats, and active LLM configuration of the RAG engine."""
    indexed_docs = list(rag_pipeline.vector_store.keys())
    total_chunks = sum(len(chunks) for chunks in rag_pipeline.vector_store.values())
    
    return {
        "status": "active",
        "pipeline_architecture": "Hybrid BM25 + Dense Semantic Chunking + LLM Grounding",
        "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "groq_model": settings.GROQ_MODEL if settings.GROQ_API_KEY else "Not Configured (Using Fallback)",
        "gemini_model": settings.GEMINI_MODEL if settings.GEMINI_API_KEY else "Not Configured (Using Fallback)",
        "indexed_documents_count": len(indexed_docs),
        "indexed_documents": indexed_docs,
        "total_vector_chunks": total_chunks
    }

@router.post("/query-rag", response_model=RAGAnswer)
async def execute_rag_query(request: RAGQueryRequest):
    """Executes a hybrid RAG query against an indexed PDF document, returning grounded answer, citation snippet, and bounding box."""
    if not request.document_name:
        raise HTTPException(status_code=400, detail="Document name is required")
    if not request.query:
        raise HTTPException(status_code=400, detail="Query string is required")

    answer = rag_pipeline.query_rag(
        doc_name=request.document_name,
        user_query=request.query
    )
    return answer

@router.post("/index-dossier/{filename}")
async def index_bidder_dossier(filename: str):
    """Chunks and indexes a specific PDF dossier into the RAG vector store."""
    demo_dir = Path(__file__).resolve().parent.parent.parent.parent / "data" / "demo_pdfs"
    demo_dir_alt = Path(__file__).resolve().parent.parent.parent / "data" / "demo_pdfs"
    
    target_path = None
    for d in [settings.UPLOAD_DIR, demo_dir, demo_dir_alt]:
        candidate = d / filename
        if candidate.exists():
            target_path = candidate
            break

    if not target_path:
        raise HTTPException(status_code=404, detail=f"PDF document '{filename}' not found in uploads or demo directories.")

    chunks = rag_pipeline.index_pdf_document(target_path)
    return {
        "status": "success",
        "filename": filename,
        "chunks_indexed": len(chunks),
        "total_tokens": sum(c.tokens_count for c in chunks)
    }
