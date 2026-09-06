from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.compliance import BidderComplianceReport

class CartelAlert(BaseModel):
    alert_id: str
    signal_name: str  # e.g., "IDENTICAL_PDF_METADATA", "TIMESTAMP_COLLUSION", "UDIN_DUPLICATION"
    severity: str = "HIGH"  # "HIGH", "CRITICAL", "MEDIUM"
    bidders_involved: List[str] = []
    forensic_evidence: str
    recommendation: str

class QCBSLeaderboardEntry(BaseModel):
    rank: int
    bidder_id: str
    company_name: str
    is_qualified: bool
    disqualification_reason: Optional[str] = None
    technical_score_ts: float  # 0 to 100
    financial_quote_inr: float
    financial_score_fs: float  # Normalized 0 to 100
    composite_score: float     # (Ts * Wt) + (Fs * Wf)
    alt_flag: bool = False     # Abnormally Low Tender
    alt_discount_pct: float = 0.0
    risk_level: str = "LOW"    # "LOW", "ELEVATED", "CRITICAL"
    lifecycle_cost_adjusted_inr: float = 0.0

class TenderEvaluationReport(BaseModel):
    tender_id: str
    tender_title: str
    issuing_authority: str
    evaluated_at: str
    total_bidders: int
    qualified_count: int
    disqualified_count: int
    cartel_alerts: List[CartelAlert] = []
    leaderboard: List[QCBSLeaderboardEntry] = []
    bidder_reports: List[BidderComplianceReport] = []
    executive_summary: str
    recommended_winner: Optional[str] = None
