from typing import List, Dict
from app.models.tender import Tender
from app.models.bidder import Bidder
from app.models.compliance import BidderComplianceReport
from app.models.report import QCBSLeaderboardEntry

class ScoringEngine:
    """
    Scoring, QCBS, and Risk Analysis Engine.
    Implements General Financial Rules (GFR) 2017 Rule 192,
    Abnormally Low Tender (ALT) detection, and Life-Cycle Cost Adjustments.
    """

    @classmethod
    def calculate_leaderboard(
        cls,
        tender: Tender,
        bidders: List[Bidder],
        compliance_reports: Dict[str, BidderComplianceReport],
        weight_tech: float = 0.70,
        weight_fin: float = 0.30
    ) -> List[QCBSLeaderboardEntry]:
        # Parse weights from tender if available (e.g. "70:30")
        if ":" in tender.qcbs_ratio:
            parts = tender.qcbs_ratio.split(":")
            try:
                wt = float(parts[0]) / 100.0
                wf = float(parts[1]) / 100.0
                weight_tech, weight_fin = wt, wf
            except Exception:
                pass

        # Find L1 among technically qualified bidders
        qualified_bidders = []
        for bidder in bidders:
            report = compliance_reports.get(bidder.id)
            if report and report.hard_gate_passed:
                qualified_bidders.append(bidder)

        min_fin_quote = min([b.total_bid_amount_inr for b in qualified_bidders]) if qualified_bidders else 0.0

        benchmark_cost = tender.estimated_cost_inr

        leaderboard_entries: List[QCBSLeaderboardEntry] = []

        for bidder in bidders:
            report = compliance_reports.get(bidder.id)
            is_qualified = report.hard_gate_passed if report else False
            disqual_reason = report.disqualification_summary if report else "Evaluation missing"
            ts = report.technical_score_ts if report else 0.0

            bid_amount = bidder.total_bid_amount_inr

            # ALT Detection: If quote is > 20% below government benchmark estimate
            alt_flag = False
            alt_discount_pct = 0.0
            if benchmark_cost > 0 and bid_amount < (benchmark_cost * 0.80):
                alt_flag = True
                alt_discount_pct = round(((benchmark_cost - bid_amount) / benchmark_cost) * 100.0, 1)

            # Financial normalization (Fs = (Fmin / F) * 100)
            if is_qualified and min_fin_quote > 0 and bid_amount > 0:
                fs = round((min_fin_quote / bid_amount) * 100.0, 2)
                composite_score = round((ts * weight_tech) + (fs * weight_fin), 2)
            else:
                fs = 0.0
                composite_score = 0.0

            # Risk level assessment (MoPNG Critical Infrastructure Safety Shield)
            if not is_qualified:
                risk_level = "CRITICAL"
                adjusted_lifecycle_cost = bid_amount * 1.5
            elif alt_flag:
                risk_level = "ELEVATED"
                # Predatory bid penalty: 30% anticipated variations + maintenance overhead
                adjusted_lifecycle_cost = round(bid_amount * 1.35, 2)
            else:
                risk_level = "LOW"
                adjusted_lifecycle_cost = round(bid_amount * 1.05, 2)

            entry = QCBSLeaderboardEntry(
                rank=0, # Will be set after sorting
                bidder_id=bidder.id,
                company_name=bidder.company_name,
                is_qualified=is_qualified,
                disqualification_reason=disqual_reason if not is_qualified else None,
                technical_score_ts=ts,
                financial_quote_inr=bid_amount,
                financial_score_fs=fs,
                composite_score=composite_score,
                alt_flag=alt_flag,
                alt_discount_pct=alt_discount_pct,
                risk_level=risk_level,
                lifecycle_cost_adjusted_inr=adjusted_lifecycle_cost
            )
            leaderboard_entries.append(entry)

        # Sort: Qualified first by composite_score DESC, then disqualified by quote
        qualified_entries = [e for e in leaderboard_entries if e.is_qualified]
        disqualified_entries = [e for e in leaderboard_entries if not e.is_qualified]

        qualified_entries.sort(key=lambda x: x.composite_score, reverse=True)
        disqualified_entries.sort(key=lambda x: x.financial_quote_inr)

        ranked_list = []
        current_rank = 1
        for e in qualified_entries:
            e.rank = current_rank
            ranked_list.append(e)
            current_rank += 1

        for e in disqualified_entries:
            e.rank = current_rank
            ranked_list.append(e)
            current_rank += 1

        return ranked_list
