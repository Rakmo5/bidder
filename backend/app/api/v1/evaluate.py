import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.report import TenderEvaluationReport
from app.api.v1.tenders import ACTIVE_TENDERS
from app.api.v1.bidders import ACTIVE_BIDDERS
from app.services.forensics_engine import ForensicsEngine
from app.services.compliance_engine import ComplianceEngine
from app.services.scoring_engine import ScoringEngine

router = APIRouter()

EVALUATION_CACHE = {}

@router.post("/run", response_model=TenderEvaluationReport)
async def run_evaluation(
    tender_id: str = Query(..., description="ID of the tender to evaluate"),
    bidder_ids: Optional[List[str]] = Query(None, description="Optional subset of bidder IDs to evaluate")
):
    if tender_id not in ACTIVE_TENDERS:
        raise HTTPException(status_code=404, detail="Tender not found")

    tender = ACTIVE_TENDERS[tender_id]

    # Selected bidders or all
    if bidder_ids:
        bidders = [ACTIVE_BIDDERS[bid] for bid in bidder_ids if bid in ACTIVE_BIDDERS]
    else:
        bidders = list(ACTIVE_BIDDERS.values())

    if not bidders:
        raise HTTPException(status_code=400, detail="No bidder dossiers available for evaluation")

    # 1. Forensics Analysis (Anti-Cartel, Duplicate UDIN, Metadata matching)
    cartel_alerts = ForensicsEngine.analyze_bidders_for_collusion(bidders)

    # 2. Compliance Evaluation
    bidder_reports = []
    compliance_map = {}
    for bidder in bidders:
        rep = ComplianceEngine.evaluate_bidder(tender, bidder)
        bidder_reports.append(rep)
        compliance_map[bidder.id] = rep

    # 3. QCBS & Risk-Adjusted Scoring
    leaderboard = ScoringEngine.calculate_leaderboard(
        tender=tender,
        bidders=bidders,
        compliance_reports=compliance_map
    )

    qualified_count = sum(1 for e in leaderboard if e.is_qualified)
    disqualified_count = len(leaderboard) - qualified_count

    # Determine recommended winner
    winner = None
    if leaderboard and leaderboard[0].is_qualified:
        winner = f"{leaderboard[0].company_name} (Rank 1, Composite Score: {leaderboard[0].composite_score})"

    exec_summary = (
        f"Technical and Financial Scrutiny completed for Tender '{tender.title}' ({tender.tender_ref}). "
        f"A total of {len(bidders)} bids were scrutinized. {qualified_count} bidders met all mandatory eligibility gates. "
        f"{disqualified_count} bidders were disqualified due to non-compliance with critical criteria (turnover/safety). "
    )
    if cartel_alerts:
        exec_summary += f"CRITICAL: {len(cartel_alerts)} potential procurement fraud / cartel signals were detected and flagged."

    report = TenderEvaluationReport(
        tender_id=tender.id,
        tender_title=tender.title,
        issuing_authority=tender.issuing_authority,
        evaluated_at=datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        total_bidders=len(bidders),
        qualified_count=qualified_count,
        disqualified_count=disqualified_count,
        cartel_alerts=cartel_alerts,
        leaderboard=leaderboard,
        bidder_reports=bidder_reports,
        executive_summary=exec_summary,
        recommended_winner=winner
    )

    EVALUATION_CACHE[tender.id] = report
    return report

@router.get("/latest/{tender_id}", response_model=TenderEvaluationReport)
async def get_latest_evaluation(tender_id: str):
    if tender_id not in EVALUATION_CACHE:
        raise HTTPException(status_code=404, detail="No evaluation generated yet for this tender")
    return EVALUATION_CACHE[tender_id]
