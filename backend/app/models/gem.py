from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GeMBidDocument(BaseModel):
    document_type: str  # e.g. "ANNUAL_TURNOVER", "EXPERIENCE_CERTIFICATE", "ISO_45001"
    filename: str
    download_url: Optional[str] = None
    sha256: Optional[str] = None

class GeMBidPackage(BaseModel):
    gem_bid_id: str = Field(..., description="GeM Bid Number, e.g. GEM/2024/B/891234")
    tender_id: str
    seller_name: str
    gem_seller_id: str
    msme_startup_status: str = "NON_MSME"  # "MICRO", "SMALL", "STARTUP", "NON_MSME"
    quoted_price_inr: float
    documents: List[GeMBidDocument] = []

class GeMEvaluationExport(BaseModel):
    gem_tender_ref: str
    ocds_release_id: str = "ocds-gem-release-2024-09"
    authority_name: str = "Ministry of Petroleum and Natural Gas (MoPNG)"
    evaluation_timestamp: str
    total_bids_received: int
    technically_qualified_sellers: List[str] = []
    disqualified_sellers: List[Dict[str, str]] = []
    recommended_contract_awardee: str
    qcbs_summary: List[Dict[str, Any]] = []
    cvc_vigilance_clearance_status: str = "CLEARED_WITH_AUDIT_TRAIL"
