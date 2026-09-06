from fastapi import APIRouter, HTTPException, Response
from app.api.v1.evaluate import EVALUATION_CACHE

router = APIRouter()

@router.get("/export/{tender_id}")
async def export_evaluation_report(tender_id: str):
    if tender_id not in EVALUATION_CACHE:
        raise HTTPException(status_code=404, detail="No evaluation found for tender")

    rep = EVALUATION_CACHE[tender_id]

    # Generate Official Government Scrutiny Note
    lines = []
    lines.append("=" * 80)
    lines.append(f"GOVERNMENT OF INDIA - {rep.issuing_authority.upper()}")
    lines.append("TENDER EVALUATION COMMITTEE (TEC) SCRUTINY NOTE & QCBS RECOMMENDATION")
    lines.append("=" * 80)
    lines.append(f"Tender Reference: {rep.tender_id}")
    lines.append(f"Tender Title:     {rep.tender_title}")
    lines.append(f"Evaluation Date:  {rep.evaluated_at}")
    lines.append("-" * 80)
    lines.append(f"Executive Summary:\n{rep.executive_summary}")
    lines.append("-" * 80)
    
    if rep.cartel_alerts:
        lines.append("\n[!] CENTRAL VIGILANCE COMMISSION (CVC) FRAUD & CARTEL ALERTS:")
        for idx, alert in enumerate(rep.cartel_alerts, 1):
            lines.append(f"  {idx}. [{alert.severity}] {alert.signal_name}")
            lines.append(f"     Bidders Involved: {', '.join(alert.bidders_involved)}")
            lines.append(f"     Forensic Evidence: {alert.forensic_evidence}")
            lines.append(f"     Recommended Action: {alert.recommendation}\n")

    lines.append("\n[+] FINAL QCBS LEADERBOARD & COMPARATIVE STATEMENT:")
    lines.append(f"{'Rank':<5} {'Company Name':<35} {'Status':<15} {'Tech (Ts)':<10} {'Quote (₹ Cr)':<14} {'Fin (Fs)':<10} {'Composite':<10} {'Risk':<10}")
    lines.append("-" * 115)
    for e in rep.leaderboard:
        status = "QUALIFIED" if e.is_qualified else "REJECTED"
        quote_cr = e.financial_quote_inr / 1e7
        lines.append(f"{e.rank:<5} {e.company_name[:34]:<35} {status:<15} {e.technical_score_ts:<10.1f} ₹{quote_cr:<12.2f} {e.financial_score_fs:<10.1f} {e.composite_score:<10.1f} {e.risk_level:<10}")

    lines.append("-" * 115)
    if rep.recommended_winner:
        lines.append(f"\nRECOMMENDED AWARD OF CONTRACT (H1 under QCBS): {rep.recommended_winner}")
    lines.append("\nSubmitted by: AI Bid Scrutiny & Compliance Verification System")
    lines.append("=" * 80)

    report_text = "\n".join(lines)

    return Response(
        content=report_text,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=TEC_Scrutiny_Report_{tender_id}.txt"}
    )
