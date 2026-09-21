import logging
from typing import Dict, Any, List
from app.ai_engine.config import ai_config
from app.ai_engine.llm_providers.groq_provider import GroqLLMProvider
from app.ai_engine.llm_providers.gemini_provider import GeminiLLMProvider
from app.models.tender import TenderRequirement, TenderBoQItem, ClauseCategory

logger = logging.getLogger(__name__)

class RequirementExtractor:
    """Extracts tender requirements, scoring weights, and BoQ line items from raw RFP documents using LLMs."""

    def __init__(self):
        self.groq_provider = GroqLLMProvider()
        self.gemini_provider = GeminiLLMProvider()

    def extract_from_text(self, tender_text: str) -> Dict[str, Any]:
        prompt_text = tender_text[:35000]
        user_prompt = f"Extract tender requirements and BoQ items from this tender text:\n\n{prompt_text}"

        # 1. Try Groq
        if self.groq_provider.is_available():
            data = self.groq_provider.generate_json(ai_config.extraction_system_prompt, user_prompt)
            if data and "requirements" in data:
                return self._parse_data(data)

        # 2. Try Gemini
        if self.gemini_provider.is_available():
            data = self.gemini_provider.generate_json(ai_config.extraction_system_prompt, user_prompt)
            if data and "requirements" in data:
                return self._parse_data(data)

        # 3. Deterministic Fallback
        return self._fallback_requirements()

    def _parse_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        reqs: List[TenderRequirement] = []
        boqs: List[TenderBoQItem] = []

        for r in data.get("requirements", []):
            try:
                cat_str = str(r.get("category", "ELIGIBILITY")).upper()
                category = getattr(ClauseCategory, cat_str, ClauseCategory.ELIGIBILITY)
                reqs.append(TenderRequirement(
                    id=str(r.get("id", f"REQ-{len(reqs)+1:03d}")),
                    category=category,
                    clause_ref=str(r.get("clause_ref", "Section II, Clause 3.1")),
                    parameter=str(r.get("parameter", "Mandatory Criterion")),
                    threshold=str(r.get("threshold", "As per Tender Document")),
                    is_mandatory=bool(r.get("is_mandatory", True)),
                    qcbs_weight=float(r.get("qcbs_weight", 10.0)),
                    description=str(r.get("description", ""))
                ))
            except Exception as e:
                logger.warning(f"Error parsing requirement item: {e}")

        for b in data.get("boq_items", []):
            try:
                boqs.append(TenderBoQItem(
                    item_code=str(b.get("item_code", f"BOQ-{len(boqs)+1:02d}")),
                    description=str(b.get("description", "Work Item")),
                    unit=str(b.get("unit", "Unit")),
                    estimated_quantity=float(b.get("estimated_quantity", 100.0)),
                    estimated_unit_rate_inr=float(b.get("estimated_unit_rate_inr", 1000.0)),
                    total_estimated_cost_inr=float(b.get("total_estimated_cost_inr", 100000.0)),
                    sor_item_ref=b.get("sor_item_ref")
                ))
            except Exception as e:
                logger.warning(f"Error parsing BoQ item: {e}")

        return {"requirements": reqs, "boq_items": boqs}

    def _fallback_requirements(self) -> Dict[str, Any]:
        from app.services.sample_data import FULL_GOVERNMENT_CRITERIA_LIBRARY
        return {
            "requirements": FULL_GOVERNMENT_CRITERIA_LIBRARY[:6],
            "boq_items": []
        }
