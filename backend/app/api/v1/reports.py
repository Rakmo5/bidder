import datetime
from fastapi import APIRouter, HTTPException, Response
from app.api.v1.evaluate import EVALUATION_CACHE
from app.api.v1.bidders import ACTIVE_BIDDERS

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

@router.get("/clarification-notice/{tender_id}/{bidder_id}")
async def generate_gfr_clarification_notice(tender_id: str, bidder_id: str):
    """Generates an official statutory GFR Rule 173 Clarification Notice with exact clause citations and 48-hour response deadline."""
    if tender_id not in EVALUATION_CACHE:
        raise HTTPException(status_code=404, detail="Evaluation not found for this tender. Run evaluation first.")
    
    rep = EVALUATION_CACHE[tender_id]
    bidder_rep = next((b for b in rep.bidder_reports if b.bidder_id == bidder_id), None)
    if not bidder_rep:
        raise HTTPException(status_code=404, detail="Bidder evaluation report not found")
    
    bidder_info = ACTIVE_BIDDERS.get(bidder_id)
    company_name = bidder_rep.company_name

    # Identify non-compliant / partial clauses
    deficiencies = []
    for item in bidder_rep.checks:
        if item.status in ["NON_COMPLIANT", "PARTIAL_DISCREPANCY", "NEEDS_HUMAN_REVIEW"]:
            deficiencies.append({
                "clause_id": item.requirement_id,
                "parameter": item.parameter,
                "citation": item.clause_ref,
                "evidence": item.evidence_snippet,
                "reason": item.rejection_reason or "Documentary condition not fulfilled"
            })

    
    now_str = datetime.datetime.now().strftime("%d-%b-%Y")
    deadline_str = (datetime.datetime.now() + datetime.timedelta(hours=48)).strftime("%d-%b-%Y %H:%M HRS IST")
    notice_ref = f"MOPNG/TEC/GFR173/2024/{bidder_id[-4:]}"

    lines = [
        "================================================================================",
        f"               GOVERNMENT OF INDIA - {rep.issuing_authority.upper()}",
        "                   TENDER EVALUATION COMMITTEE (TEC) SECRETARIAT",
        "================================================================================",
        f"Notice Ref No: {notice_ref}                               Date: {now_str}",
        "",
        "TO:",
        f"The Authorized Signatory / Managing Director",
        f"M/s {company_name}",
        f"Bidder Registration ID: {bidder_id}",
        "",
        f"SUBJECT: STATUTORY CLARIFICATION NOTICE UNDER RULE 173 OF GENERAL FINANCIAL RULES (GFR 2017)",
        f"TENDER REF: {tender_id} - '{rep.tender_title}'",
        "--------------------------------------------------------------------------------",
        "",
        "Sir / Madam,",
        "",
        "1. During technical scrutiny of the bid submitted by your firm against the subject tender,",
        "   the Tender Evaluation Committee (TEC) observed the following discrepancies / non-compliances:",
        ""
    ]

    if deficiencies:
        for idx, d in enumerate(deficiencies, 1):
            lines.append(f"   [{idx}] Parameter: {d['parameter']}")
            lines.append(f"       Clause Reference: {d['citation']}")
            lines.append(f"       Scrutiny Finding: {d['reason']}")
            lines.append(f"       Extracted Document Proof: \"{d['evidence']}\"")
            lines.append("")
    else:
        lines.append("   - Your bid prima facie meets all threshold criteria. This notice confirms pre-award verification.")
        lines.append("")

    lines.extend([
        "2. In terms of GFR 2017 Rule 173 and MoPNG Procurement Guidelines, you are hereby called upon",
        f"   to furnish necessary clarification and authenticated documentary evidence within 48 HOURS",
        f"   (i.e., on or before {deadline_str}) via the GeM Portal / e-Procurement Portal.",
        "",
        "3. Please note that no modification in the substantive financial or technical terms of your bid",
        "   shall be permitted. Failure to respond within the stipulated timeline will result in the TEC",
        "   evaluating your tender based solely on records already submitted, which may lead to summary rejection.",
        "",
        "Yours faithfully,",
        "",
        "Digitally Signed by:",
        "Dr. Priya Sharma",
        "Technical Scrutinizer / Senior Procurement Officer",
        f"Tender Evaluation Committee, {rep.issuing_authority}",
        "================================================================================"
    ])

    notice_text = "\n".join(lines)
    return {
        "notice_ref": notice_ref,
        "tender_id": tender_id,
        "bidder_id": bidder_id,
        "company_name": company_name,
        "generated_date": now_str,
        "response_deadline": deadline_str,
        "deficiencies_count": len(deficiencies),
        "deficiencies": deficiencies,
        "notice_text": notice_text
    }

