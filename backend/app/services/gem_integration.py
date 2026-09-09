import datetime
from typing import Dict, Any, List
from app.models.report import TenderEvaluationReport
from app.models.gem import GeMEvaluationExport, GeMBidPackage

class GeMIntegrationService:
    @staticmethod
    def export_to_gem_schema(report: TenderEvaluationReport) -> GeMEvaluationExport:
        qualified = [e.company_name for e in report.leaderboard if e.is_qualified]
        disqualified = [
            {"seller_name": e.company_name, "rejection_ground": e.disqualification_reason or "Mandatory gate deficit"}
            for e in report.leaderboard if not e.is_qualified
        ]

        qcbs_items = [
            {
                "rank": e.rank,
                "seller_name": e.company_name,
                "technical_score_ts": e.technical_score_ts,
                "quoted_amount_inr": e.financial_quote_inr,
                "financial_score_fs": e.financial_score_fs,
                "composite_qcbs_score": e.composite_score,
                "abnormally_low_tender_flag": e.alt_flag,
                "risk_profile": e.risk_level
            }
            for e in report.leaderboard
        ]

        return GeMEvaluationExport(
            gem_tender_ref=f"GEM/2024/RA/{report.tender_id}",
            ocds_release_id=f"ocds-213qz3-GEM-{report.tender_id}",
            authority_name=report.issuing_authority,
            evaluation_timestamp=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            total_bids_received=report.total_bidders,
            technically_qualified_sellers=qualified,
            disqualified_sellers=disqualified,
            recommended_contract_awardee=report.recommended_winner or "None",
            qcbs_summary=qcbs_items,
            cvc_vigilance_clearance_status="CLEARED_WITH_AUDIT_TRAIL" if not report.cartel_alerts else "VIGILANCE_REVIEW_FLAGGED"
        )
