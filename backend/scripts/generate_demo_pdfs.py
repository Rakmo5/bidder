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
    fontSize=16,
    leading=20,
    textColor=colors.HexColor("#123769"),
    alignment=1, # Center
    spaceAfter=15
)
heading_style = ParagraphStyle(
    'DocHeading',
    parent=styles['Heading2'],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#0f4c81"),
    spaceBefore=10,
    spaceAfter=8
)
body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#1e293b")
)
callout_style = ParagraphStyle(
    'DocCallout',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#095c37"),
    backColor=colors.HexColor("#f0fdf4"),
    borderColor=colors.HexColor("#86efac"),
    borderWidth=1,
    borderPadding=6,
    spaceBefore=6,
    spaceAfter=6
)

def create_tender_pdf():
    pdf_path = OUTPUT_DIR / "Tender_MoPNG_30km_Gas_Pipeline.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    # Title & Header
    story.append(Paragraph("GOVERNMENT OF INDIA<br/>MINISTRY OF PETROLEUM AND NATURAL GAS (MoPNG)", title_style))
    story.append(Paragraph("<b>GLOBAL TENDER INVITATION: EPC OF 30 KM HIGH-PRESSURE NATURAL GAS PIPELINE</b>", heading_style))
    story.append(Paragraph("<b>Tender Reference:</b> MoPNG/GAIL/PIPELINE/2024/09 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Estimated Cost:</b> INR 32.70 Crore &nbsp;&nbsp;|&nbsp;&nbsp; <b>QCBS Ratio:</b> 70:30", body_style))
    story.append(Spacer(1, 15))

    # Section I: Eligibility Criteria
    story.append(Paragraph("SECTION III (SCC) — MANDATORY ELIGIBILITY & SCRUTINY CRITERIA", heading_style))
    story.append(Paragraph("Bidders must satisfy all mandatory thresholds to qualify for technical evaluation. Non-compliance results in immediate disqualification.", body_style))
    story.append(Spacer(1, 8))

    criteria_data = [
        ["Clause Ref", "Parameter", "Threshold Condition", "Mandatory?", "Max Marks"],
        ["SCC 3.2", "Annual Turnover", "Minimum INR 15.00 Crore average in last 3 FY (FY21, FY22, FY23) certified by CA with valid UDIN.", "YES", "15"],
        ["SCC 4.1", "Past Experience", "Minimum 5.0 years experience with at least 1 pipeline contract >= 25 km completed for PSU/Govt.", "YES", "25"],
        ["HSE 7.1", "ISO 45001 Safety", "Valid active ISO 45001:2018 certification in Oil & Gas works as on bid closing date.", "YES", "15"],
        ["Sec V 8.3", "Plant & Machinery", "Ownership/lease of minimum 2 Automatic External Pipe Clamps & Induction Bending Unit.", "NO", "20"],
        ["ITB 9.1", "EMD / Bid Security", "INR 25,00,000 via irrevocable Bank Guarantee valid for 180 days.", "YES", "10"],
        ["ITB 12.4", "Integrity Pact", "Notarized Non-Blacklisting affidavit on INR 100 non-judicial stamp paper affirming no CVC debarment.", "YES", "15"]
    ]
    t = Table(criteria_data, colWidths=[65, 110, 240, 65, 55])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#123769")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Page 2: BoQ
    story.append(PageBreak())
    story.append(Paragraph("SECTION VI — BILL OF QUANTITIES (BoQ) SCHEDULE OF RATES", heading_style))
    story.append(Paragraph("Estimated Engineering Rates baseline as per CPWD / MoPNG Schedule of Rates (SOR 2024):", body_style))
    story.append(Spacer(1, 8))

    boq_data = [
        ["Item Code", "Work Description", "Unit", "Qty", "Est. Unit Rate (INR)", "Total Estimated (INR)"],
        ["BOQ-01", "Trenching, stringing, welding 24-inch API 5L X-65 pipe", "Km", "30.0", "85,00,000", "25,50,00,000"],
        ["BOQ-02", "Horizontal Directional Drilling (HDD) for river crossing", "Meter", "1200.0", "45,000", "5,40,00,000"],
        ["BOQ-03", "Hydrotesting, pre-commissioning, nitrogen purging", "Lot", "1.0", "1,80,00,000", "1,80,00,000"],
        ["TOTAL", "Total Estimated Project Value (DPR Baseline)", "", "", "", "32,70,00,000"]
    ]
    t2 = Table(boq_data, colWidths=[60, 220, 45, 45, 80, 85])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f4c81")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f1f5f9")),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t2)
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder1_pdf():
    pdf_path = OUTPUT_DIR / "Bidder1_LT_Hydrocarbon_Engineering.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("LARSEN & TOUBRO HYDROCARBON ENGINEERING LTD", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: L99999MH1946PLC004768 &nbsp;|&nbsp; GSTIN: 27AAACL1234F1Z8", body_style))
    story.append(Spacer(1, 10))

    # Turnover
    story.append(Paragraph("ANNEXURE I: STATUTORY AUDITOR TURNOVER CERTIFICATE", heading_style))
    story.append(Paragraph("This is to certify that M/s Larsen & Toubro Hydrocarbon Engineering Ltd has achieved the following annual turnover:", body_style))
    story.append(Spacer(1, 4))
    
    fin_data = [
        ["Financial Year", "Audited Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 22.00 Crore", "INR 85.00 Crore", "Sharma & Co Chartered Accountants"],
        ["FY 2021-22", "INR 26.00 Crore", "INR 88.50 Crore", "Sharma & Co Chartered Accountants"],
        ["FY 2022-23", "INR 25.50 Crore", "INR 92.00 Crore", "Sharma & Co Chartered Accountants"],
        ["Average 3-Yr", "INR 24.50 Crore", "INR 88.50 Crore", "ICAI UDIN: 23104588AAAA129481"]
    ]
    t = Table(fin_data, colWidths=[90, 130, 130, 185])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#123769")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Paragraph("<b>Auditor Certification:</b> Statutory Auditor Certificate issued by Sharma & Co: Certified average turnover INR 24.50 Cr with valid ICAI UDIN 23104588AAAA129481.", callout_style))
    story.append(Spacer(1, 10))

    # Experience & ISO
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II & III: PAST EXPERIENCE & ISO 45001 SAFETY CERTIFICATE", heading_style))
    story.append(Paragraph("<b>Experience Track Record:</b> 11.5 Years in Hydrocarbon Pipeline EPC. Successfully completed 35 km cross-country pipeline for GAIL India Ltd (Contract Value: INR 48.2 Cr).", body_style))
    story.append(Paragraph("<b>ISO 45001:2018 Certificate:</b> Certificate No: OHS-9941-IND, Accredited by TUV Rheinland, valid through 15-May-2027.", callout_style))
    story.append(Paragraph("<b>Plant & Machinery:</b> 4 units Automatic External Pipe Clamps, 1 unit Induction Bending Rig 24-inch (Outright Ownership).", body_style))
    story.append(Paragraph("<b>Total Quoted Financial Bid:</b> INR 31,80,00,000 (INR 31.80 Crore) &nbsp;|&nbsp; EMD Bank Guarantee: BG-SBI-2024-8871 for INR 25,00,000.", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder2_pdf():
    pdf_path = OUTPUT_DIR / "Bidder2_Apex_InfraTech_Ltd.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("APEX INFRATECH PRIVATE LIMITED", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: U45200DL2018PTC334511 &nbsp;|&nbsp; GSTIN: 07AACCA9988G1Z1", body_style))
    story.append(Spacer(1, 10))

    # Turnover Deficit
    story.append(Paragraph("ANNEXURE I: AUDITED FINANCIAL STATEMENTS", heading_style))
    fin_data = [
        ["Financial Year", "Audited Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 10.50 Crore", "INR 4.50 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2021-22", "INR 11.50 Crore", "INR 4.80 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2022-23", "INR 11.60 Crore", "INR 5.20 Crore", "GS & Partners Chartered Accountants"],
        ["Average 3-Yr", "INR 11.20 Crore", "INR 4.83 Crore", "ICAI UDIN: 23049182BBBB912831"]
    ]
    t = Table(fin_data, colWidths=[90, 130, 130, 185])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991b1b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Paragraph("<b>Turnover Note:</b> Form 3CA/3CD: Turnover reported as INR 11.20 Cr for qualifying assessment years (Shortfall against INR 15.00 Cr mandatory threshold).", body_style))
    story.append(Spacer(1, 10))

    # Expired ISO
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II: QUALITY & SAFETY ACCREDITATION", heading_style))
    story.append(Paragraph("<b>ISO 45001:2018 Certificate:</b> Certificate No: OHS-APX-441 issued by Intertek India, expired on 10-Aug-2022. No renewal endorsement attached.", body_style))
    story.append(Paragraph("<b>Experience Track Record:</b> 6.0 Years in civil pipelaying works.", body_style))
    story.append(Paragraph("<b>Total Quoted Financial Bid:</b> INR 28,50,00,000 (INR 28.50 Crore).", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

def create_bidder3_pdf():
    pdf_path = OUTPUT_DIR / "Bidder3_Zenith_Piping_Corp.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("ZENITH PIPING & ENERGY CORPORATION", title_style))
    story.append(Paragraph("<b>TECHNICAL & FINANCIAL BID DOSSIER</b> &nbsp;|&nbsp; CIN: U28112DL2019PTC345678 &nbsp;|&nbsp; GSTIN: 07AAACZ1122D1Z9", body_style))
    story.append(Spacer(1, 10))

    # Financials with DUPLICATE UDIN matching Bidder 2
    story.append(Paragraph("ANNEXURE I: STATUTORY AUDITOR CERTIFICATE", heading_style))
    fin_data = [
        ["Financial Year", "Audited Turnover (INR)", "Net Worth (INR)", "Statutory Auditor"],
        ["FY 2020-21", "INR 16.00 Crore", "INR 5.20 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2021-22", "INR 17.50 Crore", "INR 5.80 Crore", "GS & Partners Chartered Accountants"],
        ["FY 2022-23", "INR 16.90 Crore", "INR 6.10 Crore", "GS & Partners Chartered Accountants"],
        ["Average 3-Yr", "INR 16.80 Crore", "INR 5.70 Crore", "ICAI UDIN: 23049182BBBB912831"] # DUPLICATE UDIN
    ]
    t = Table(fin_data, colWidths=[90, 130, 130, 185])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#d97706")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Predatory quote
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE II: TECHNICAL COMPLIANCE & FINANCIAL BID", heading_style))
    story.append(Paragraph("<b>ISO 45001:2018 Certificate:</b> Certificate No: DNV-GL-9988, Valid until 30-Mar-2026.", body_style))
    story.append(Paragraph("<b>Experience:</b> 5.5 Years in gas pipeline jointing.", body_style))
    story.append(Paragraph("<b>Financial Bid:</b> INR 19,80,00,000 (INR 19.80 Crore) — <b>39.4% Discount against DPR Baseline</b> (Triggers Abnormally Low Tender Surcharge).", body_style))
    
    doc.build(story)
    print(f"Created: {pdf_path}")

if __name__ == "__main__":
    create_tender_pdf()
    create_bidder1_pdf()
    create_bidder2_pdf()
    create_bidder3_pdf()
    print("All 4 Demo PDFs created successfully in data/demo_pdfs/")
