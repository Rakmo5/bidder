import sys
import os
import io
from pathlib import Path

# Fix Windows console encoding for UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.rag_engine import rag_pipeline
from app.core.config import settings

def run_rag_demo():
    print("=" * 80)
    print("[AI] AUTONOMOUS AI & RAG PIPELINE DEMONSTRATION")
    print("     Hybrid BM25 + Dense Semantic Chunking + LLM Grounding Engine")
    print("=" * 80)
    print(f"* Active LLM Provider: {settings.DEFAULT_LLM_PROVIDER}")
    print(f"* Groq Model:          {settings.GROQ_MODEL if settings.GROQ_API_KEY else 'Fallback Heuristics'}")
    print(f"* Gemini Model:        {settings.GEMINI_MODEL if settings.GEMINI_API_KEY else 'Fallback Heuristics'}")
    print("-" * 80)

    demo_dir = Path(__file__).resolve().parent.parent.parent / "data" / "demo_pdfs"
    if not demo_dir.exists():
        print(f"[!] Demo dir not found at {demo_dir}")
        return

    # 1. Index available PDFs
    print("\n[STEP 1] Indexing PDF Dossiers into RAG Vector Store:")
    pdf_files = list(demo_dir.glob("*.pdf"))
    if not pdf_files:
        print("  [!] No PDFs found. Please generate them first.")
        return

    for pdf in pdf_files:
        chunks = rag_pipeline.index_pdf_document(pdf)
        total_tokens = sum(c.tokens_count for c in chunks)
        print(f"  + Indexed '{pdf.name}' -> {len(chunks)} chunks ({total_tokens} tokens)")

    # 2. Execute RAG Queries
    print("\n" + "=" * 80)
    print("[STEP 2] Executing Live RAG Queries Against Bidder Submissions:")
    print("=" * 80)

    test_queries = [
        ("Bidder1_LT_Hydrocarbon_Engineering.pdf", "What is the average 3-year turnover and the ICAI UDIN number of L&T?"),
        ("Bidder1_LT_Transportation_Infrastructure.pdf", "What is the civil turnover and slipform sensor paver fleet owned by L&T?"),
        ("Bidder2_Apex_Highway_Builders.pdf", "What is the status and expiry date of the ISO 45001 safety certificate?"),
        ("Bidder3_Zenith_Expressways_Corp.pdf", "What is the quoted financial bid amount and the discount against DPR estimate?")
    ]

    for doc_name, query in test_queries:
        if not (demo_dir / doc_name).exists():
            continue

        print(f"\n[FILE] Target Document: {doc_name}")
        print(f"[QUERY] Audit Query:   \"{query}\"")
        print("-" * 80)

        # Retrieve & synthesize
        result = rag_pipeline.query_rag(doc_name, query)

        print(f"[SYNTHESIS] ({result.llm_provider_used}):")
        print(f"   Answer: \"{result.answer}\"")
        print(f"   Grounded Evidence: \"{result.grounded_evidence}\"")
        print(f"   Exact Page & BBox: Page {result.page_number} | Bounding Box: {result.normalized_bbox}")
        print(f"   Confidence Score:  {result.confidence_score * 100:.1f}%")
        print(f"   Retrieved Chunks ({len(result.retrieved_chunks)}):")
        for idx, r in enumerate(result.retrieved_chunks, 1):
            print(f"      [{idx}] (Score: {r.similarity_score}) Page {r.chunk.page_number}: \"{r.chunk.text[:90]}...\"")

    print("\n" + "=" * 80)
    print(">>> AI & RAG PIPELINE DEMONSTRATION COMPLETE 100%! <<<")
    print("=" * 80)

if __name__ == "__main__":
    run_rag_demo()
