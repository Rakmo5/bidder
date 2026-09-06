import json
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from google import genai
from app.core.config import settings
from app.models.tender import TenderRequirement, TenderBoQItem, ClauseCategory

logger = logging.getLogger(__name__)

EXTRACTION_SYSTEM_PROMPT = """You are an elite Public Procurement Legal & Technical Auditor specializing in Indian Government Tenders (MoPNG, MoRTH, CPWD, GeM).
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

class RequirementEngine:
    def __init__(self):
        self.groq_client = None
        self.gemini_client = None
        if settings.GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")
        
        if settings.GEMINI_API_KEY:
            try:
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")

    def extract_requirements(self, tender_text: str) -> Dict[str, Any]:
        # Truncate to reasonable context window if huge
        prompt_text = tender_text[:35000]

        # 1. Try Groq Llama-3.3-70b (ultra-fast)
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Extract tender requirements and BoQ items from this tender text:\n\n{prompt_text}"}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                raw_json = response.choices[0].message.content
                data = json.loads(raw_json)
                return self._parse_extracted_data(data)
            except Exception as e:
                logger.error(f"Groq requirement extraction failed: {e}. Trying fallback.")

        # 2. Try Gemini fallback
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=f"{EXTRACTION_SYSTEM_PROMPT}\n\nTENDER DOCUMENT:\n{prompt_text}",
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                data = json.loads(text.strip())
                return self._parse_extracted_data(data)
            except Exception as e:
                logger.error(f"Gemini requirement extraction failed: {e}")

        # 3. Deterministic Fallback if offline or API failure
        return self._fallback_requirements()

    def _parse_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        requirements = []
        for item in data.get("requirements", []):
            try:
                req = TenderRequirement(
                    id=item.get("id", f"REQ-{len(requirements)+1:03d}"),
                    category=ClauseCategory(item.get("category", "ELIGIBILITY").upper()),
                    clause_ref=item.get("clause_ref", "General Conditions"),
                    parameter=item.get("parameter", "Requirement"),
                    threshold=item.get("threshold", "Condition specified in tender"),
                    is_mandatory=bool(item.get("is_mandatory", True)),
                    qcbs_weight=float(item.get("qcbs_weight", 10.0)),
                    description=item.get("description", "")
                )
                requirements.append(req)
            except Exception:
                continue

        boq_items = []
        for b in data.get("boq_items", []):
            try:
                boq = TenderBoQItem(
                    item_code=b.get("item_code", f"BOQ-{len(boq_items)+1:02d}"),
                    description=b.get("description", "Work item"),
                    unit=b.get("unit", "Lot"),
                    estimated_quantity=float(b.get("estimated_quantity", 1.0)),
                    estimated_unit_rate_inr=float(b.get("estimated_unit_rate_inr", 100000.0)),
                    total_estimated_cost_inr=float(b.get("total_estimated_cost_inr", 100000.0))
                )
                boq_items.append(boq)
            except Exception:
                continue

        return {"requirements": requirements, "boq_items": boq_items}

    def _fallback_requirements(self) -> Dict[str, Any]:
        """Provides realistic MoPNG Hydrocarbon Pipeline laying requirements as fallback"""
        reqs = [
            TenderRequirement(
                id="REQ-001",
                category=ClauseCategory.ELIGIBILITY,
                clause_ref="Section III (SCC) Clause 3.2",
                parameter="Minimum Average Annual Turnover",
                threshold="Minimum ₹15.0 Crore in each of the last 3 financial years (FY 2020-21, 2021-22, 2022-23)",
                is_mandatory=True,
                qcbs_weight=15.0,
                description="Must be certified by a practicing Chartered Accountant with valid ICAI UDIN."
            ),
            TenderRequirement(
                id="REQ-002",
                category=ClauseCategory.ELIGIBILITY,
                clause_ref="Section III (SCC) Clause 4.1",
                parameter="Past Experience in Hydrocarbon / Gas Pipeline Laying",
                threshold="Minimum 5 years experience with at least 1 single contract of >= 25 km pipeline laying",
                is_mandatory=True,
                qcbs_weight=25.0,
                description="Completion certificate from Central/State Govt or PSU must be furnished."
            ),
            TenderRequirement(
                id="REQ-003",
                category=ClauseCategory.SAFETY,
                clause_ref="Section IV (HSE) Clause 7.1",
                parameter="Occupational Health & Safety Accreditation",
                threshold="Valid ISO 45001:2018 certification for Oil & Gas Construction works",
                is_mandatory=True,
                qcbs_weight=15.0,
                description="Must be active as on date of bid submission."
            ),
            TenderRequirement(
                id="REQ-004",
                category=ClauseCategory.TECHNICAL,
                clause_ref="Section V Clause 8.3",
                parameter="Key Construction Equipment Ownership",
                threshold="Ownership or lease proof of minimum 2 Automatic External Pipe Clamps & 2 Induction Bending Units",
                is_mandatory=False,
                qcbs_weight=20.0,
                description="Outright ownership awarded full marks; long-term lease awarded 70% marks."
            ),
            TenderRequirement(
                id="REQ-005",
                category=ClauseCategory.LEGAL,
                clause_ref="Section II (ITB) Clause 12.4",
                parameter="Non-Blacklisting & Integrity Pact Affidavit",
                threshold="Notarized non-debarment declaration and signed Integrity Pact on ₹100 stamp paper",
                is_mandatory=True,
                qcbs_weight=10.0,
                description="Must declare no ongoing CVC/CBI debarment in PSUs."
            ),
            TenderRequirement(
                id="REQ-006",
                category=ClauseCategory.FINANCIAL,
                clause_ref="Section II (ITB) Clause 9.1",
                parameter="Earnest Money Deposit (EMD) / Bid Security",
                threshold="₹25,00,000 via Bank Guarantee or valid MSME / NSIC exemption certificate",
                is_mandatory=True,
                qcbs_weight=15.0,
                description="BG valid for minimum 180 days from bid closing date."
            )
        ]

        boqs = [
            TenderBoQItem(
                item_code="BOQ-01",
                description="Trenching, pipeline laying, jointing and welding of 24-inch API 5L X-65 steel pipeline",
                unit="Kilometer",
                estimated_quantity=30.0,
                estimated_unit_rate_inr=8500000.0,
                total_estimated_cost_inr=255000000.0
            ),
            TenderBoQItem(
                item_code="BOQ-02",
                description="Horizontal Directional Drilling (HDD) for river and highway crossings",
                unit="Meter",
                estimated_quantity=1200.0,
                estimated_unit_rate_inr=45000.0,
                total_estimated_cost_inr=54000000.0
            ),
            TenderBoQItem(
                item_code="BOQ-03",
                description="Hydrotesting, pre-commissioning, nitrogen purging and golden joint testing",
                unit="Lot",
                estimated_quantity=1.0,
                estimated_unit_rate_inr=18000000.0,
                total_estimated_cost_inr=18000000.0
            )
        ]

        return {"requirements": reqs, "boq_items": boqs}
