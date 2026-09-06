from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ClauseCategory(str, Enum):
    ELIGIBILITY = "ELIGIBILITY"       # Mandatory binary gate (e.g. Turnover, Solvency, Min Years)
    TECHNICAL = "TECHNICAL"           # Scored / technical competence (e.g. Equipment, Pipeline welding specs)
    FINANCIAL = "FINANCIAL"           # EMD, Net Worth, Bank Guarantee
    LEGAL = "LEGAL"                   # Blacklisting affidavit, Joint Venture restrictions
    SAFETY = "SAFETY"                 # ISO 45001, OHSAS, incident-free record

class TenderRequirement(BaseModel):
    id: str = Field(..., description="Unique Requirement ID, e.g. REQ-001")
    category: ClauseCategory = Field(default=ClauseCategory.ELIGIBILITY)
    clause_ref: str = Field(..., description="Tender Section and Clause number, e.g. Section III, SCC 4.2")
    parameter: str = Field(..., description="Name of the parameter, e.g. Minimum Annual Financial Turnover")
    threshold: str = Field(..., description="Quantitative or qualitative threshold, e.g. >= ₹15 Crore in each of last 3 FY")
    is_mandatory: bool = Field(default=True, description="True if non-compliance warrants immediate disqualification")
    qcbs_weight: float = Field(default=10.0, description="Max marks for this criterion in Technical Evaluation (0-100 scale)")
    description: Optional[str] = None

class TenderBoQItem(BaseModel):
    item_code: str
    description: str
    unit: str
    estimated_quantity: float
    estimated_unit_rate_inr: float
    total_estimated_cost_inr: float

class Tender(BaseModel):
    id: str
    title: str
    issuing_authority: str = "Ministry of Petroleum and Natural Gas (MoPNG)"
    tender_ref: str
    estimated_cost_inr: float
    emd_amount_inr: float
    qcbs_ratio: str = "70:30"  # 70% Quality, 30% Cost
    requirements: List[TenderRequirement] = []
    boq_items: List[TenderBoQItem] = []
    created_at: Optional[str] = None
