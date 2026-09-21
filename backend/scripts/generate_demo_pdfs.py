import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "demo_pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=15,
    leading=19,
    textColor=colors.HexColor("#065f46"),
    alignment=1, # Center
    spaceAfter=12
)
heading_style = ParagraphStyle(
    'DocHeading',
    parent=styles['Heading2'],
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#047857"),
    spaceBefore=8,
    spaceAfter=6
)
body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#1e293b")
)
callout_style = ParagraphStyle(
    'DocCallout',
    parent=styles['Normal'],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#065f46"),
    backColor=colors.HexColor("#ecfdf5"),
    borderColor=colors.HexColor("#6ee7b7"),
    borderWidth=1,
    borderPadding=5,
    spaceBefore=5,
    spaceAfter=5
)

def create_tender_pdf():
    pdf_path = OUTPUT_DIR / "Tender_MoRTH_4Lane_Highway_EPC.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    story = []

    # Title & Header
    story.append(Paragraph("GOVERNMENT OF INDIA<br/>MINISTRY OF ROAD TRANSPORT AND HIGHWAYS (MoRTH) / NHAI", title_style))
    story.append(Paragraph("<b>NATIONAL COMPETITIVE BIDDING: EPC OF 4-LANE GREENFIELD HIGHWAY BYPASS (28.4 KM / 113.6 LANE-KM)</b>", heading_style))
    story.append(Paragraph("<b>Tender Reference:</b> MoRTH/NHAI/EXP/2024/402 &nbsp;|&nbsp; <b>Estimated Cost:</b> INR 72.13 Crore &nbsp;|&nbsp; <b>Evaluation:</b> QCBS (70:30 Quality-to-Cost)", body_style))
    story.append(Spacer(1, 10))

    # Section I: Eligibility & Highway Engineering Standards
    story.append(Paragraph("SECTION III (SCC) — STATUTORY ELIGIBILITY & HIGHWAY QUALITY BENCHMARKS", heading_style))
    story.append(Paragraph("Bids are scrutinized strictly under GFR 2017 Rule 173 and IRC:37-2018 / IRC:SP:84-2019 standards to prevent premature pavement degradation and monsoon washouts.", body_style))
    story.append(Spacer(1, 6))

    criteria_data = [
        ["Clause Ref", "Highway Technical Parameter", "Threshold Benchmark Condition", "Mandatory?", "Weight"],
        ["SCC 2.1", "Civil Highway Turnover", "Minimum INR 25.00 Crore average in last 3 FY certified by CA with valid ICAI UDIN.", "YES", "15%"],
        ["SCC 3.1", "Past 4-Lane EPC Experience", "Minimum 5.0 years with at least 1 completed 4-lane highway contract >= 20.0 km.", "YES", "20%"],
        ["MoRTH 500", "Sensor Paver Machinery", "Ownership of minimum 2 Electronic Sensor Pavers (9m width) & 1 Slipform Concrete Paver.", "YES", "20%"],
        ["HSE 7.2", "Road Safety & ISO 45001", "Active ISO 45001:2018 and ISO 9001:2015 safety accreditation on bid opening date.", "YES", "15%"],
        ["ITB 8.2", "EMD / Bid Security", "INR 50,00,000 via irrevocable Bank Guarantee valid for 180 days.", "YES", "10%"],
        ["EPC 17.1", "5-Year Defect Liability (DLP)", "Notarized guarantee for 60 months Defect Liability Period backed by 5% Performance Security.", "YES", "20%"]
    ]
    t = Table(criteria_data, colWidths=[65, 125, 235, 60, 45])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#065f46")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Page 2: BoQ Schedule of Rates (SOR)
    story.append(PageBreak())
    story.append(Paragraph("SECTION VI — BILL OF QUANTITIES (BoQ) HIGHWAY SCHEDULE OF RATES", heading_style))
    story.append(Paragraph("Engineering baseline unit rates derived from MoRTH Standard Data Book & IRC:37 Pavement Design for 150 MSA traffic load:", body_style))
    story.append(Spacer(1, 6))

    boq_data = [
        ["Item Code", "Highway Work Item Description", "Unit", "Est. Qty", "Est. Rate (INR)", "Total Estimated (INR)"],
        ["BOQ-HW-01", "Earthwork excavation, embankment formation & subgrade CBR >= 8%", "Cum", "2,50,000", "280.00", "7,00,00,000"],
        ["BOQ-HW-02", "Dense Bituminous Macadam (DBM) with VG-40 Bitumen (75mm)", "Cum", "45,000", "8,500.00", "38,25,00,000"],
        ["BOQ-HW-03", "Bituminous Concrete (BC) wearing course (Polymer Modified CRMB-60)", "Cum", "24,000", "11,200.00", "26,88,00,000"],
        ["TOTAL", "Total Estimated Project Value (DPR Baseline)", "", "", "", "72,13,00,000"]
    ]
    t2 = Table(boq_data, colWidths=[65, 225, 35, 55, 75, 80])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#047857")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f1f5f9")),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t2)
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder1_pdf():
    pdf_path = OUTPUT_DIR / "Bidder1_LT_Transportation_Infrastructure.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    story = []

    story.append(Paragraph("L&T TRANSPORTATION INFRASTRUCTURE LIMITED", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: L99999MH1946PLC004768 &nbsp;|&nbsp; GSTIN: 27AAACL1234F1Z8", body_style))
    story.append(Spacer(1, 8))

    # Turnover
    story.append(Paragraph("ANNEXURE I: STATUTORY AUDITOR CERTIFICATE & FINANCIAL PROFILE", heading_style))
    story.append(Paragraph("Certified audited turnover statement for EPC highway infrastructure projects in India:", body_style))
    story.append(Spacer(1, 4))
    
    fin_data = [
        ["Financial Year", "Audited Civil Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 62.00 Crore", "INR 185.00 Crore", "Deloitte Haskins & Sells LLP"],
        ["FY 2021-22", "INR 68.00 Crore", "INR 185.00 Crore", "Deloitte Haskins & Sells LLP"],
        ["FY 2022-23", "INR 71.00 Crore", "INR 185.00 Crore", "Deloitte Haskins & Sells LLP"],
        ["Average 3-Yr", "INR 67.00 Crore", "INR 185.00 Crore", "ICAI UDIN: 24081923AAAA998811"]
    ]
    t = Table(fin_data, colWidths=[90, 130, 120, 195])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#065f46")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Paragraph("<b>Auditor Certification:</b> Issued by Deloitte Haskins & Sells LLP. Certified 3-yr average turnover INR 67.00 Cr with valid ICAI UDIN 24081923AAAA998811 (Exceeds INR 25.00 Cr threshold).", callout_style))
    story.append(Spacer(1, 8))

    # Experience & ISO
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II & III: PAST HIGHWAY EXPERIENCE & SAFETY CERTIFICATES", heading_style))
    story.append(Paragraph("<b>Highway Experience Track Record:</b> 12.5 Years in Expressways & National Highways EPC. Completed 48.6 km 4-lane Greenfield bypass for NHAI (Value: INR 142.5 Cr).", body_style))
    story.append(Paragraph("<b>ISO 45001:2018 & ISO 9001:2015:</b> Certificate No: OHS-9941-IND, Accredited by TUV Rheinland, valid through 15-May-2027.", callout_style))
    story.append(Paragraph("<b>Paving Fleet:</b> 2x Wirtgen SP-64 Slipform Pavers, 1x Ammann 160 TPH Hot Mix Plant, 3x Vogele Super 1800-3 SprayJet Sensor Pavers (All Outright Owned).", body_style))
    story.append(Paragraph("<b>Total Quoted Financial Bid:</b> INR 70,61,00,000 (INR 70.61 Crore) &nbsp;|&nbsp; EMD Bank Guarantee: BG-SBI-2024-8871 for INR 50,00,000.", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder2_pdf():
    pdf_path = OUTPUT_DIR / "Bidder2_Apex_Highway_Builders.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    story = []

    story.append(Paragraph("APEX HIGHWAY BUILDERS & INFRATECH LTD", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: U45200DL2018PTC334511 &nbsp;|&nbsp; GSTIN: 07AACCA9988G1Z1", body_style))
    story.append(Spacer(1, 8))

    # Turnover
    story.append(Paragraph("ANNEXURE I: AUDITED FINANCIAL STATEMENTS", heading_style))
    fin_data = [
        ["Financial Year", "Audited Civil Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 26.00 Crore", "INR 11.00 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2021-22", "INR 28.00 Crore", "INR 11.00 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2022-23", "INR 27.50 Crore", "INR 11.00 Crore", "GS & Partners Chartered Accountants"],
        ["Average 3-Yr", "INR 27.16 Crore", "INR 11.00 Crore", "ICAI UDIN: 23049182BBBB912831"]
    ]
    t = Table(fin_data, colWidths=[90, 130, 120, 195])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991b1b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Paragraph("<b>Turnover Summary:</b> 3-Yr Average Turnover INR 27.16 Cr certified by GS & Partners with UDIN 23049182BBBB912831.", body_style))
    story.append(Spacer(1, 8))

    # Expired ISO
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II: QUALITY & SAFETY ACCREDITATION", heading_style))
    story.append(Paragraph("<b>ISO 45001:2018 Safety Certificate:</b> Certificate No: OHS-APX-441 issued by Intertek India, <b>expired on 10-Aug-2022</b>. No valid renewal endorsement attached.", body_style))
    story.append(Paragraph("<b>Highway Experience:</b> 6.0 Years in state road construction.", body_style))
    story.append(Paragraph("<b>Machinery:</b> Hired manual mini-pavers without electronic slope sensing sensors.", body_style))
    story.append(Paragraph("<b>Total Quoted Financial Bid:</b> INR 65,84,00,000 (INR 65.84 Crore).", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder3_pdf():
    pdf_path = OUTPUT_DIR / "Bidder3_Zenith_Expressways_Corp.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    story = []

    story.append(Paragraph("ZENITH EXPRESSWAYS & ROADWAYS CORP", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: U28112DL2019PTC345678 &nbsp;|&nbsp; GSTIN: 07AAACZ1122D1Z9", body_style))
    story.append(Spacer(1, 8))

    # Financials with DUPLICATE UDIN matching Bidder 2
    story.append(Paragraph("ANNEXURE I: STATUTORY AUDITOR CERTIFICATE", heading_style))
    fin_data = [
        ["Financial Year", "Audited Civil Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 28.00 Crore", "INR 9.50 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2021-22", "INR 29.00 Crore", "INR 9.50 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2022-23", "INR 28.50 Crore", "INR 9.50 Crore", "GS & Partners Chartered Accountants"],
        ["Average 3-Yr", "INR 28.50 Crore", "INR 9.50 Crore", "ICAI UDIN: 23049182BBBB912831"] # DUPLICATE UDIN
    ]
    t = Table(fin_data, colWidths=[90, 130, 120, 195])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#d97706")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Predatory quote
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II: TECHNICAL COMPLIANCE & FINANCIAL BID", heading_style))
    story.append(Paragraph("<b>ISO 45001:2018 Certificate:</b> Certificate No: DNV-GL-9988, Valid until 30-Mar-2026.", body_style))
    story.append(Paragraph("<b>Experience:</b> 5.5 Years in flexible road surfacing.", body_style))
    story.append(Paragraph("<b>Financial Bid:</b> INR 46,25,00,000 (INR 46.25 Crore) — <b>35.9% Below DPR Baseline</b> (Abnormally Low Tender - Underquoted Bitumen and Subgrade Compaction by 39%).", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

if __name__ == "__main__":
    create_tender_pdf()
    create_bidder1_pdf()
    create_bidder2_pdf()
    create_bidder3_pdf()
    print("All 4 MoRTH Highway Demo PDFs created successfully in data/demo_pdfs/")
