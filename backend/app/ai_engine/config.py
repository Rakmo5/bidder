import os
from pydantic import BaseModel
from app.core.config import settings

class AIConfig(BaseModel):
    """Central configuration for AI models, prompts, chunk sizes, and similarity thresholds."""
    
    # Model Providers
    default_provider: str = settings.DEFAULT_LLM_PROVIDER
    groq_api_key: str = settings.GROQ_API_KEY
    gemini_api_key: str = settings.GEMINI_API_KEY
    
    # Model Names
    groq_primary_model: str = settings.GROQ_MODEL
    groq_fast_model: str = settings.FAST_GROQ_MODEL
    gemini_primary_model: str = settings.GEMINI_MODEL
    
    # Chunking & Retrieval Parameters
    chunk_size_tokens: int = 300
    chunk_overlap_tokens: int = 50
    bm25_k1: float = 1.5
    bm25_b: float = 0.75
    top_k_retrieval: int = 3
    cartel_similarity_threshold: float = 0.80

    # System Prompts
    rag_system_prompt: str = """You are an elite Public Procurement Legal & Technical Auditor for Indian Government Tenders (MoPNG / MoRTH / CVC).
Answer the user's specific audit question based ONLY on the retrieved document context below.
Provide a direct, concise fact-grounded answer, and cite the exact phrase that proves it.

Output strictly valid JSON with this schema:
{
  "answer": "Direct factual response (e.g. Average annual civil turnover is INR 67.00 Crore authenticated by CA with UDIN 24081923AAAA998811).",
  "grounded_evidence": "Exact quoted sentence from the text proving this fact.",
  "confidence_score": 0.98
}"""

    extraction_system_prompt: str = """You are an elite Public Procurement Legal & Technical Auditor specializing in Indian Government Tenders (MoPNG, MoRTH, CPWD, GeM).
Your duty is to extract all mandatory eligibility thresholds, technical scoring parameters, and Bill of Quantities (BoQ) items from the provided tender text.

Return your response strictly as a valid JSON object matching this schema:
{
  "requirements": [
    {
      "id": "REQ-001",
      "category": "ELIGIBILITY" | "TECHNICAL" | "FINANCIAL" | "LEGAL" | "SAFETY",
      "clause_ref": "Exact Section / Clause (e.g., Section II, Clause 3.1)",
      "parameter": "Concise parameter title (e.g., Minimum Average Annual Turnover)",
      "threshold": "Exact condition (e.g., >= INR 15.0 Crore in each of last 3 FY)",
      "is_mandatory": true | false,
      "qcbs_weight": 10.0,
      "description": "Brief context"
    }
  ],
  "boq_items": [
    {
      "item_code": "BOQ-01",
      "description": "Detailed line item description",
      "unit": "Meter / MT / Lot",
      "estimated_quantity": 1000.0,
      "estimated_unit_rate_inr": 25000.0,
      "total_estimated_cost_inr": 25000000.0
    }
  ]
}

DO NOT wrap in markdown fences or include conversational commentary. Output pure valid JSON."""

ai_config = AIConfig()
