from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ClauseCategory(str, Enum):
    ELIGIBILITY = "ELIGIBILITY"       # Mandatory binary gate (e.g. Turnover, Solvency, Min Experience)
    TECHNICAL = "TECHNICAL"           # Scored / technical competence (e.g. Slipform Pavers, Batching Plant capacity)
    FINANCIAL = "FINANCIAL"           # EMD, Net Worth, Bank Solvency
    LEGAL = "LEGAL"                   # Non-blacklisting affidavit, CVC integrity pact
    SAFETY_QUALITY = "SAFETY_QUALITY" # ISO 9001, ISO 45001, IRC Q-Marks, NABL lab accreditation

class TenderRequirement(BaseModel):
    id: str = Field(..., description="Unique Requirement ID, e.g. REQ-MORTH-01")
    category: ClauseCategory = Field(default=ClauseCategory.ELIGIBILITY)
    clause_ref: str = Field(..., description="Tender Section and Clause number, e.g. Section III, SCC 4.2 / IRC:37")
    parameter: str = Field(..., description="Name of the parameter, e.g. Aggregate Impact Value (AIV) & Bitumen Grade")
    threshold: str = Field(..., description="Quantitative or qualitative threshold, e.g. >= ₹25 Crore turnover or VG-40 bitumen")
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
    sor_item_ref: Optional[str] = "MoRTH Standard Data Book 2024"

class Tender(BaseModel):
    id: str
    title: str
    issuing_authority: str = "Ministry of Road Transport and Highways (MoRTH) / NHAI"
    tender_ref: str
    project_type: str = "4-Lane Greenfield Highway EPC (Rigid & Flexible Pavement)"
    length_km: float = 28.4
    lane_km: float = 113.6
    design_life_years: int = 20
    design_traffic_msa: float = 150.0  # Million Standard Axles
    pavement_type: str = "Rigid Pavement (PQC M-40) + Heavy Duty DBM Sub-base"
    estimated_cost_inr: float
    emd_amount_inr: float
    qcbs_ratio: str = "70:30"  # 70% Quality, 30% Cost (Preventing L1 Monsoon Failure)
    standards_compliance: str = "IRC:37-2018 / IRC:SP:84-2019 / MoRTH 5th Revision"
    requirements: List[TenderRequirement] = []
    boq_items: List[TenderBoQItem] = []
    created_at: Optional[str] = None

