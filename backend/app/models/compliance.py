from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ComplianceStatus(str, Enum):
    COMPLIANT = "COMPLIANT"                         # 🟢 Meets or exceeds condition
    NON_COMPLIANT = "NON_COMPLIANT"                 # 🔴 Fails threshold / Missing proof
    PARTIAL_DISCREPANCY = "PARTIAL_DISCREPANCY"     # 🟡 Minor discrepancy / Expired cert
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"       # ⚪ Complex legal clause requiring manual sign-off

class ComplianceCheckItem(BaseModel):
    requirement_id: str
    parameter: str
    clause_ref: str
    is_mandatory: bool
    status: ComplianceStatus
    claimed_value: str
    evidence_snippet: str = Field(..., description="Direct quote extracted from bidder PDF")
    evidence_document: str = Field(..., description="Filename containing the proof")
    evidence_page: int = Field(default=1, description="Page number of the evidence")
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)
    rejection_reason: Optional[str] = None
    technical_marks_awarded: float = 0.0
    technical_marks_max: float = 0.0

class BidderComplianceReport(BaseModel):
    bidder_id: str
    company_name: str
    hard_gate_passed: bool = True
    disqualification_summary: Optional[str] = None
    technical_score_ts: float = 0.0
    technical_score_max: float = 100.0
    checks: List[ComplianceCheckItem] = []
