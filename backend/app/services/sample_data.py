from typing import List, Dict
from app.models.tender import Tender, TenderRequirement, TenderBoQItem, ClauseCategory
from app.models.bidder import Bidder, FinancialProfile, Certificate, BidderBoQQuote, DocumentMetadata

# ==============================================================================
# 1. COMPREHENSIVE HIGHWAY & MoRTH / IRC CRITERIA STANDARDS LIBRARY (12 PILLARS)
# ==============================================================================
FULL_GOVERNMENT_CRITERIA_LIBRARY: List[TenderRequirement] = [
    TenderRequirement(
        id="STD-MORTH-01",
        category=ClauseCategory.ELIGIBILITY,
        clause_ref="GFR Rule 173 / MoRTH SCC 3.1",
        parameter="Average Annual Civil Highway Turnover",
        threshold="Minimum 30% of estimated tender value (INR 25.00 Crore) over last 3 audited FY certified by CA with ICAI UDIN",
        is_mandatory=True,
        qcbs_weight=15.0,
        description="Statutory financial capability gate under General Financial Rules (GFR 2017)."
    ),
    TenderRequirement(
        id="STD-MORTH-02",
        category=ClauseCategory.ELIGIBILITY,
        clause_ref="IRC:SP:84 / MoRTH SCC 4.1",
        parameter="Past Technical Experience in 4/6-Lane Highway EPC",
        threshold="Minimum 5.0 years with at least one completed 4-lane highway contract >= 20 km or value >= 80% tender value",
        is_mandatory=True,
        qcbs_weight=20.0,
        description="Verifiable performance certificate from NHAI, MoRTH, or State PWD."
    ),
    TenderRequirement(
        id="STD-MORTH-03",
        category=ClauseCategory.TECHNICAL,
        clause_ref="MoRTH Section 500 / IRC:37",
        parameter="Electronic Sensor Paver & Slipform Machinery",
        threshold="Ownership of minimum 2 Electronic Sensor Pavers (9m width) and 1 Automatic Slipform Concrete Paver",
        is_mandatory=True,
        qcbs_weight=15.0,
        description="Mandatory machinery to ensure uniform riding quality, compaction, and zero premature pothole formation."
    ),
    TenderRequirement(
        id="STD-MORTH-04",
        category=ClauseCategory.TECHNICAL,
        clause_ref="MoRTH Section 100 Clause 112",
        parameter="SCADA-Enabled Hot Mix / Concrete Batching Plant",
        threshold="Ownership or captive lease of minimum 1 Hot Mix Plant (>= 120 TPH) and 1 Concrete Batching Plant (>= 60 m3/hr)",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="Automated computerized batch recording prevents bitumen cheating and aggregate gradation errors."
    ),
    TenderRequirement(
        id="STD-MORTH-05",
        category=ClauseCategory.TECHNICAL,
        clause_ref="IRC:37-2018 Clause 5.2",
        parameter="Subgrade California Bearing Ratio (CBR) & Compaction",
        threshold="Subgrade laboratory test verifying CBR >= 8% with 97% Modified Proctor Density compaction",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="Core foundation benchmark. Prevents pavement subsidence and mud pumping during monsoon."
    ),
    TenderRequirement(
        id="STD-MORTH-06",
        category=ClauseCategory.TECHNICAL,
        clause_ref="IS:73 / MoRTH Section 504",
        parameter="Bitumen Viscosity Grade & Polymer Modification",
        threshold="Strict usage of VG-40 or Crumb Rubber / Polymer Modified Bitumen (CRMB-60) for wearing courses",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="High softening point bitumen prevents rutting in summer and water ingress during heavy rains."
    ),
    TenderRequirement(
        id="STD-MORTH-07",
        category=ClauseCategory.SAFETY_QUALITY,
        clause_ref="IRC:SP:88 Road Safety Norms",
        parameter="Occupational Health, Safety & ISO 45001 Certification",
        threshold="Active ISO 45001:2018 and ISO 9001:2015 certification with certified Traffic Safety Management Lead",
        is_mandatory=True,
        qcbs_weight=5.0,
        description="IAF/NABCB accredited certification verifying work zone barricading and worker safety."
    ),
    TenderRequirement(
        id="STD-MORTH-08",
        category=ClauseCategory.SAFETY_QUALITY,
        clause_ref="MoRTH Section 900 Clause 901",
        parameter="NABL-Accredited On-Site Quality Control Lab",
        threshold="Commitment to establish fully equipped on-site testing lab with NABL calibrated compressive & core testing machines",
        is_mandatory=False,
        qcbs_weight=5.0,
        description="Enables continuous 24/7 testing of core samples, bitumen extraction, and aggregate impact value."
    ),
    TenderRequirement(
        id="STD-MORTH-09",
        category=ClauseCategory.TECHNICAL,
        clause_ref="MoRTH Prequalification Schedule D",
        parameter="Key Highway Engineers & Pavement Specialists",
        threshold="Resident Project Director (>= 15 yrs exp in 4-lane highways), Senior Pavement Specialist, Safety Lead",
        is_mandatory=False,
        qcbs_weight=5.0,
        description="Evaluated on years of relevant NHAI/MoRTH highway project leadership."
    ),
    TenderRequirement(
        id="STD-MORTH-10",
        category=ClauseCategory.FINANCIAL,
        clause_ref="CVC Manual / MoRTH SCC 3.4",
        parameter="Bank Solvency & Net Worth Certificate",
        threshold="Positive net worth in last 3 FY and Bank Solvency Certificate >= INR 28.00 Crore (40% of tender value)",
        is_mandatory=True,
        qcbs_weight=5.0,
        description="Issued by Scheduled Commercial Bank within 6 months of bid submission."
    ),
    TenderRequirement(
        id="STD-MORTH-11",
        category=ClauseCategory.FINANCIAL,
        clause_ref="Section II (ITB) Clause 8.2",
        parameter="Earnest Money Deposit (EMD) / Bid Security",
        threshold="INR 50,00,000 via irrevocable Bank Guarantee valid for 180 days from bid opening date",
        is_mandatory=True,
        qcbs_weight=5.0,
        description="Statutory procurement security."
    ),
    TenderRequirement(
        id="STD-MORTH-12",
        category=ClauseCategory.LEGAL,
        clause_ref="MoRTH EPC Model Agreement Clause 17.1",
        parameter="5-Year Defect Liability & Maintenance Undertaking",
        threshold="Notarized undertaking guaranteeing 60 months Defect Liability Period (DLP) backed by 5% Performance Security",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="Contractor legally bound to repair potholes, cracks, and surface failures at zero cost to public."
    )
]

# ==============================================================================
# 2. PRIMARY MoRTH NATIONAL HIGHWAY EPC TENDER
# ==============================================================================
def get_sample_morth_tender() -> Tender:
    reqs = [
        TenderRequirement(
            id="REQ-MORTH-01",
            category=ClauseCategory.ELIGIBILITY,
            clause_ref="Section III (SCC) Clause 2.1",
            parameter="Average Annual Financial Turnover (Highway Works)",
            threshold="INR 25.00 Crore minimum average in last 3 FY (FY21, FY22, FY23) authenticated by CA with UDIN",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Civil highway infrastructure turnover."
        ),
        TenderRequirement(
            id="REQ-MORTH-02",
            category=ClauseCategory.ELIGIBILITY,
            clause_ref="Section III (SCC) Clause 3.1",
            parameter="Past Experience in 4/6-Lane Bituminous Highways",
            threshold="Minimum 5.0 years with at least one completed 4-lane highway project of length >= 20 km",
            is_mandatory=True,
            qcbs_weight=20.0,
            description="Completion certificate from NHAI, MoRTH or State PWD."
        ),
        TenderRequirement(
            id="REQ-MORTH-03",
            category=ClauseCategory.TECHNICAL,
            clause_ref="IRC:37 & MoRTH Section 500",
            parameter="Paving Plant & Electronic Sensor Pavers",
            threshold="Ownership of minimum 1 Hot Mix Plant (>= 120 TPH) and 2 Electronic Sensor Pavers (9m width)",
            is_mandatory=True,
            qcbs_weight=20.0,
            description="Critical requirement to prevent uneven road surface and premature potholing."
        ),
        TenderRequirement(
            id="REQ-MORTH-04",
            category=ClauseCategory.SAFETY_QUALITY,
            clause_ref="HSE & Traffic Safety Norms",
            parameter="Road Safety & Quality Accreditation",
            threshold="Valid ISO 9001:2015 & ISO 45001:2018 with certified Traffic Management Lead",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Active safety accreditation on opening date."
        ),
        TenderRequirement(
            id="REQ-MORTH-05",
            category=ClauseCategory.FINANCIAL,
            clause_ref="ITB Clause 8.2",
            parameter="Earnest Money Deposit (EMD)",
            threshold="INR 50,00,000 via irrevocable Bank Guarantee valid for 180 days",
            is_mandatory=True,
            qcbs_weight=10.0,
            description="Scheduled Commercial Bank Guarantee."
        ),
        TenderRequirement(
            id="REQ-MORTH-06",
            category=ClauseCategory.LEGAL,
            clause_ref="MoRTH Prequalification Norms",
            parameter="5-Year Defect Liability & Maintenance Guarantee",
            threshold="Formal commitment to 60 Months Defect Liability Period backed by 5% Performance Security",
            is_mandatory=True,
            qcbs_weight=20.0,
            description="Mandatory structural performance guarantee."
        )
    ]

    boqs = [
        TenderBoQItem(
            item_code="BOQ-HW-01",
            description="Earthwork excavation, embankment formation & subgrade compaction (CBR >= 8%, 500mm)",
            unit="Cum",
            estimated_quantity=250000.0,
            estimated_unit_rate_inr=280.0,
            total_estimated_cost_inr=70000000.0,
            sor_item_ref="MoRTH SOR Item 3.1"
        ),
        TenderBoQItem(
            item_code="BOQ-HW-02",
            description="Dense Bituminous Macadam (DBM) with VG-40 Viscosity Bitumen (75mm compacted thickness)",
            unit="Cum",
            estimated_quantity=45000.0,
            estimated_unit_rate_inr=8500.0,
            total_estimated_cost_inr=382500000.0,
            sor_item_ref="MoRTH SOR Item 5.4"
        ),
        TenderBoQItem(
            item_code="BOQ-HW-03",
            description="Bituminous Concrete (BC) wearing course with polymer modified bitumen (40mm thickness)",
            unit="Cum",
            estimated_quantity=24000.0,
            estimated_unit_rate_inr=11200.0,
            total_estimated_cost_inr=268800000.0,
            sor_item_ref="MoRTH SOR Item 5.7"
        )
    ]

    return Tender(
        id="MORTH-NH-2024-402",
        title="Construction of 4-Lane Greenfield National Highway Bypass Section (28.4 km) under EPC Mode",
        issuing_authority="Ministry of Road Transport and Highways (MoRTH) / NHAI",
        tender_ref="MoRTH/NHAI/EXP/2024/402",
        project_type="4-Lane Greenfield Highway EPC (Rigid & Flexible Pavement)",
        length_km=28.4,
        lane_km=113.6,
        design_life_years=20,
        design_traffic_msa=150.0,
        pavement_type="Rigid Pavement (PQC M-40) + Heavy Duty DBM Sub-base",
        estimated_cost_inr=721300000.0,
        emd_amount_inr=5000000.0,
        qcbs_ratio="70:30",
        standards_compliance="IRC:37-2018 / IRC:SP:84-2019 / MoRTH 5th Revision",
        requirements=reqs,
        boq_items=boqs,
        created_at="2024-09-02"
    )

# Alias for backward compatibility
get_sample_mopng_tender = get_sample_morth_tender

# ==============================================================================
# 3. HIGHWAY CONTRACTORS DATASET
# ==============================================================================
def get_sample_bidders() -> List[Bidder]:
    # Contractor 1: L&T Transportation Infrastructure (Recommended Winner - High Quality)
    b1 = Bidder(
        id="BID-01",
        company_name="L&T Transportation Infrastructure Ltd",
        gstin="27AAACL1234F1Z8",
        cin="L99999MH1946PLC004768",
        years_experience=12.5,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=620000000.0,
            turnover_fy22_inr=680000000.0,
            turnover_fy23_inr=710000000.0,
            average_turnover_inr=670000000.0,
            net_worth_inr=1850000000.0,
            ca_name="Deloitte Haskins & Sells LLP",
            ca_firm="Deloitte Haskins & Sells LLP",
            ca_udin="24081923AAAA998811",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="TUV Rheinland", valid_until="2027-05-15", is_active=True, page_number=2),
            Certificate(name="ISO 9001:2015", issuing_body="Bureau Veritas", valid_until="2026-11-20", is_active=True, page_number=2),
            Certificate(name="NABL Accredited Quality Lab", issuing_body="NABL India", valid_until="2026-08-10", is_active=True, page_number=2)
        ],
        machinery_owned=[
            "Wirtgen SP-64 Slipform Concrete Paver (2 units)",
            "Ammann Apollo 160 TPH Asphalt Hot Mix Plant",
            "Vogele Super 1800-3 SprayJet Sensor Paver (3 units)",
            "Hamm 311 Compaction Rollers with GPS density sensors (6 units)"
        ],
        key_personnel=[
            "Dr. V. Raman (32 yrs exp - Chief Highway Project Director)",
            "Er. K. Sundaram (Pavement Design Lead, M.Tech IIT Bombay)",
            "S. Narayanan (Safety Lead, NEBOSH Certified)"
        ],
        boq_quotes=[
            BidderBoQQuote(item_code="BOQ-HW-01", description="Earthwork excavation & subgrade CBR >= 8%", quoted_unit_rate_inr=275.0, total_quoted_cost_inr=68750000.0),
            BidderBoQQuote(item_code="BOQ-HW-02", description="Dense Bituminous Macadam (DBM) with VG-40", quoted_unit_rate_inr=8350.0, total_quoted_cost_inr=375750000.0),
            BidderBoQQuote(item_code="BOQ-HW-03", description="Bituminous Concrete (BC) wearing course", quoted_unit_rate_inr=10900.0, total_quoted_cost_inr=261600000.0)
        ],
        total_bid_amount_inr=706100000.0,
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder1_LT_Transportation_Infrastructure.pdf",
                author="L&T Transportation Engineering Division",
                creator="Adobe InDesign 2024 (Windows)",
                producer="Adobe PDF Library 17.0",
                creation_date="2024-09-02T10:15:30Z",
                page_count=2,
                sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            )
        ]
    )

    # Contractor 2: Apex Highway Builders (Failed Safety / Shared Workstation Collusion)
    b2 = Bidder(
        id="BID-02",
        company_name="Apex Highway Builders & InfraTech Ltd",
        gstin="07AACCA9988G1Z1",
        cin="U45200DL2018PTC334511",
        years_experience=6.0,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=260000000.0,
            turnover_fy22_inr=280000000.0,
            turnover_fy23_inr=275000000.0,
            average_turnover_inr=271666666.0,
            net_worth_inr=110000000.0,
            ca_name="GS & Partners Chartered Accountants",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="Intertek India", valid_until="2022-08-10", is_active=False, page_number=2),
            Certificate(name="ISO 9001:2015", issuing_body="Intertek India", valid_until="2025-01-15", is_active=True, page_number=2)
        ],
        machinery_owned=[
            "Hired Manual Mini-Pavers (No electronic slope sensors)",
            "Batching Plant 30 m3/hr (Non-SCADA)"
        ],
        key_personnel=["S. Singhania (8 yrs exp)"],
        boq_quotes=[
            BidderBoQQuote(item_code="BOQ-HW-01", description="Earthwork excavation & subgrade CBR >= 8%", quoted_unit_rate_inr=260.0, total_quoted_cost_inr=65000000.0),
            BidderBoQQuote(item_code="BOQ-HW-02", description="Dense Bituminous Macadam (DBM) with VG-40", quoted_unit_rate_inr=7800.0, total_quoted_cost_inr=351000000.0),
            BidderBoQQuote(item_code="BOQ-HW-03", description="Bituminous Concrete (BC) wearing course", quoted_unit_rate_inr=10100.0, total_quoted_cost_inr=242400000.0)
        ],
        total_bid_amount_inr=658400000.0,
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder2_Apex_Highway_Builders.pdf",
                author="NHAI-BIDDER-WORKSTATION-09",
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z",
                page_count=2,
                sha256="c8f18e9064f786968032777ad11832049d5c8ab3f3458ef4feadba00c5c3690d"
            )
        ]
    )

    # Contractor 3: Zenith Expressways (Predatory ALT Suicide Bidder / Monsoon Failure Risk)
    b3 = Bidder(
        id="BID-03",
        company_name="Zenith Expressways & Roadways Corp",
        gstin="07AAACZ1122D1Z9",
        cin="U28112DL2019PTC345678",
        years_experience=5.5,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=280000000.0,
            turnover_fy22_inr=290000000.0,
            turnover_fy23_inr=285000000.0,
            average_turnover_inr=285000000.0,
            net_worth_inr=95000000.0,
            ca_name="GS & Partners",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831", # DUPLICATE UDIN matching Bidder 2
            udin_valid=False
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="DNV GL", valid_until="2026-03-30", is_active=True, page_number=2)
        ],
        machinery_owned=["Manual Asphalt Paver (1 unit)"],
        key_personnel=["R. K. Mehra (10 yrs exp)"],
        boq_quotes=[
            # Predatory Abnormally Low Tender (ALT) rates - Cuts corners on Bitumen & Compaction
            BidderBoQQuote(item_code="BOQ-HW-01", description="Earthwork excavation (Compromised CBR < 5%)", quoted_unit_rate_inr=170.0, total_quoted_cost_inr=42500000.0), # -39% ALT
            BidderBoQQuote(item_code="BOQ-HW-02", description="Dense Bituminous Macadam (Low grade Bitumen)", quoted_unit_rate_inr=5200.0, total_quoted_cost_inr=234000000.0), # -38.8% ALT
            BidderBoQQuote(item_code="BOQ-HW-03", description="Bituminous Concrete (Substandard Binder)", quoted_unit_rate_inr=7750.0, total_quoted_cost_inr=186000000.0) # -30.8% ALT
        ],
        total_bid_amount_inr=462500000.0, # -35.9% Abnormally Low Tender (L1 trap)
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder3_Zenith_Expressways_Corp.pdf",
                author="NHAI-BIDDER-WORKSTATION-09", # IDENTICAL AUTHOR matching Bidder 2
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z", # EXACT SAME SECOND matching Bidder 2
                page_count=2,
                sha256="fa488b0244de82cc78627b46bbdf5888d3e8e19e7555adce7f8dcf62551cf182"
            )
        ]
    )

    return [b1, b2, b3]
