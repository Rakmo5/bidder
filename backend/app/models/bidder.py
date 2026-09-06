from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class DocumentMetadata(BaseModel):
    filename: str
    author: Optional[str] = "Unknown"
    creator: Optional[str] = "Unknown"
    producer: Optional[str] = "Unknown"
    creation_date: Optional[str] = None
    mod_date: Optional[str] = None
    page_count: int = 1
    sha256: Optional[str] = None

class FinancialProfile(BaseModel):
    turnover_fy21_inr: float = 0.0
    turnover_fy22_inr: float = 0.0
    turnover_fy23_inr: float = 0.0
    average_turnover_inr: float = 0.0
    net_worth_inr: float = 0.0
    ca_name: Optional[str] = None
    ca_firm: Optional[str] = None
    ca_udin: Optional[str] = None
    udin_valid: bool = False

class Certificate(BaseModel):
    name: str  # e.g. "ISO 9001:2015", "ISO 45001:2018", "ASME Section IX"
    issuing_body: str
    valid_until: Optional[str] = None
    is_active: bool = True
    page_number: Optional[int] = 1

class BidderBoQQuote(BaseModel):
    item_code: str
    description: str
    quoted_unit_rate_inr: float
    total_quoted_cost_inr: float

class Bidder(BaseModel):
    id: str
    company_name: str
    gstin: Optional[str] = None
    cin: Optional[str] = None
    years_experience: float = 0.0
    financial_profile: FinancialProfile = Field(default_factory=FinancialProfile)
    certificates: List[Certificate] = []
    machinery_owned: List[str] = []
    key_personnel: List[str] = []
    boq_quotes: List[BidderBoQQuote] = []
    total_bid_amount_inr: float = 0.0
    documents_metadata: List[DocumentMetadata] = []
    raw_text: Optional[str] = None
