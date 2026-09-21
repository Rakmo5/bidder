import logging
from typing import Dict, Any, List
from app.ai_engine.pipeline.rag_pipeline import RAGPipeline
from app.models.compliance import ComplianceCheckItem, ComplianceStatus
from app.models.tender import TenderRequirement
from app.models.bidder import Bidder

logger = logging.getLogger(__name__)

class ClauseVerifier:
    """Verifies compliance of a bidder against a specific tender requirement using Grounded RAG."""

    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline

    def verify_requirement(self, requirement: TenderRequirement, bidder: Bidder) -> ComplianceCheckItem:
        doc_name = bidder.documents[0].filename if bidder.documents else "Bidder_Dossier.pdf"
        query = f"Verify whether bidder meets requirement '{requirement.parameter}' with threshold '{requirement.threshold}'"

        rag_result = self.rag_pipeline.query(doc_name, query)

        return ComplianceCheckItem(
            requirement_id=requirement.id,
            clause_ref=requirement.clause_ref,
            parameter=requirement.parameter,
            is_mandatory=requirement.is_mandatory,
            status=ComplianceStatus.COMPLIANT if rag_result.confidence_score > 0.6 else ComplianceStatus.PARTIAL_DISCREPANCY,
            claimed_value="Documentary Evidence Verified",
            evidence_snippet=rag_result.grounded_evidence,
            evidence_document=doc_name,
            evidence_page=rag_result.page_number,
            confidence_score=rag_result.confidence_score,
            technical_marks_awarded=requirement.qcbs_weight if rag_result.confidence_score > 0.6 else 0.0,
            technical_marks_max=requirement.qcbs_weight,
            rejection_reason=None if rag_result.confidence_score > 0.6 else "Documentary shortfall identified during scrutiny"
        )
