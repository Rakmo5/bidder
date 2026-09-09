from typing import List, Dict
from app.models.tender import Tender, TenderRequirement, TenderBoQItem, ClauseCategory
from app.models.bidder import Bidder, FinancialProfile, Certificate, BidderBoQQuote, DocumentMetadata

# ==============================================================================
# 1. COMPREHENSIVE GOVERNMENT CRITERIA STANDARDS LIBRARY (12 PILLARS)
# ==============================================================================
FULL_GOVERNMENT_CRITERIA_LIBRARY: List[TenderRequirement] = [
    TenderRequirement(
        id="STD-01",
        category=ClauseCategory.ELIGIBILITY,
        clause_ref="GFR Rule 173 / SCC 3.1",
        parameter="Average Annual Financial Turnover",
        threshold="Minimum 30% of estimated tender value over last 3 audited FY (certified by CA with ICAI UDIN)",
        is_mandatory=True,
        qcbs_weight=15.0,
        description="Statutory minimum benchmark as per General Financial Rules (GFR 2017)."
    ),
    TenderRequirement(
        id="STD-02",
        category=ClauseCategory.ELIGIBILITY,
        clause_ref="CPWD / SCC 4.1",
        parameter="Past Technical Experience in Similar Works",
        threshold="Minimum 5.0 years with at least 1 completed contract of >= 80% tender value or 2 contracts >= 50%",
        is_mandatory=True,
        qcbs_weight=20.0,
        description="Verifiable completion certificates from Central/State Govt or PSUs."
    ),
    TenderRequirement(
        id="STD-03",
        category=ClauseCategory.FINANCIAL,
        clause_ref="CVC Manual / SCC 3.4",
        parameter="Net Worth & Solvency Certificate",
        threshold="Positive net worth in each of last 3 FY and Bank Solvency Certificate of >= 40% tender value",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="Issued by Scheduled Commercial Bank within last 6 months."
    ),
    TenderRequirement(
        id="STD-04",
        category=ClauseCategory.SAFETY,
        clause_ref="HSE Manual 7.1",
        parameter="Occupational Health & Safety Accreditation",
        threshold="Active ISO 45001:2018 (or OHSAS 18001) certification as on bid submission closing date",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="NABCB / IAF accredited certifying body."
    ),
    TenderRequirement(
        id="STD-05",
        category=ClauseCategory.TECHNICAL,
        clause_ref="ISO 9001 Quality Norms",
        parameter="Quality Management System Accreditation",
        threshold="Valid ISO 9001:2015 certification for project design, procurement, and execution",
        is_mandatory=False,
        qcbs_weight=10.0,
        description="Full marks for active certification."
    ),
    TenderRequirement(
        id="STD-06",
        category=ClauseCategory.SAFETY,
        clause_ref="MoEFCC Norms",
        parameter="Environmental Management Accreditation",
        threshold="Valid ISO 14001:2015 certification for environmental compliance",
        is_mandatory=False,
        qcbs_weight=5.0,
        description="Awarded for green construction compliance."
    ),
    TenderRequirement(
        id="STD-07",
        category=ClauseCategory.TECHNICAL,
        clause_ref="Section V Schedule C",
        parameter="Heavy Construction Plant & Machinery Ownership",
        threshold="Outright ownership or committed lease of core plant equipment (Automatic clamps, pavers, batching plants)",
        is_mandatory=False,
        qcbs_weight=15.0,
        description="100% marks for outright ownership; 70% marks for confirmed long-term lease."
    ),
    TenderRequirement(
        id="STD-08",
        category=ClauseCategory.TECHNICAL,
        clause_ref="Section V Schedule D",
        parameter="Key Technical Personnel & CV Credentials",
        threshold="Project Director (>= 15 yrs exp), Safety Officer (NEBOSH/B.Tech), Quality Control Lead",
        is_mandatory=False,
        qcbs_weight=10.0,
        description="Evaluation based on years of experience in similar high-value projects."
    ),
    TenderRequirement(
        id="STD-09",
        category=ClauseCategory.FINANCIAL,
        clause_ref="ITB Clause 9.1",
        parameter="Earnest Money Deposit (EMD) / Bid Security",
        threshold="2% of estimated tender value via Bank Guarantee or valid MSME/NSIC exemption",
        is_mandatory=True,
        qcbs_weight=5.0,
        description="BG valid for minimum 180 days from opening date."
    ),
    TenderRequirement(
        id="STD-10",
        category=ClauseCategory.LEGAL,
        clause_ref="ITB Clause 12.4",
        parameter="Non-Blacklisting Affidavit & Integrity Pact",
        threshold="Notarized affidavit on INR 100 stamp paper affirming zero CVC/CBI debarment + signed Integrity Pact",
        is_mandatory=True,
        qcbs_weight=5.0,
        description="Mandatory statutory integrity compliance."
    ),
    TenderRequirement(
        id="STD-11",
        category=ClauseCategory.LEGAL,
        clause_ref="DPIIT Public Procurement Order",
        parameter="Make in India (Local Content Preference)",
        threshold="Class-I Local Supplier declaration with >= 50% domestic value addition certificate",
        is_mandatory=False,
        qcbs_weight=5.0,
        description="Statutory purchase preference under Make in India policy."
    ),
    TenderRequirement(
        id="STD-12",
        category=ClauseCategory.TECHNICAL,
        clause_ref="GCC Clause 33",
        parameter="Defect Liability Period (DLP) Commitment",
        threshold="60 Months (5 Years) comprehensive defect liability commitment backed by 5% Performance Security",
        is_mandatory=True,
        qcbs_weight=10.0,
        description="Mandatory guarantee against premature structural failure."
    )
]

# ==============================================================================
# 2. MoPNG HYDROCARBON PIPELINE TENDER
# ==============================================================================
def get_sample_mopng_tender() -> Tender:
    reqs = [
        TenderRequirement(
            id="REQ-001",
            category=ClauseCategory.ELIGIBILITY,
            clause_ref="Section III (SCC) Clause 3.2",
            parameter="Minimum Average Annual Turnover",
            threshold="INR 15.00 Crore minimum over last 3 audited financial years (FY21, FY22, FY23)",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Must be authenticated by Statutory Auditor with 18-digit ICAI UDIN."
        ),
        TenderRequirement(
            id="REQ-002",
            category=ClauseCategory.ELIGIBILITY,
            clause_ref="Section III (SCC) Clause 4.1",
            parameter="Past Experience in Hydrocarbon Pipeline Laying",
            threshold="Minimum 5.0 years with at least one executed pipeline contract of length >= 25 km",
            is_mandatory=True,
            qcbs_weight=25.0,
            description="Completion certificate from PSU (IOCL, ONGC, GAIL) or Central Ministry required."
        ),
        TenderRequirement(
            id="REQ-003",
            category=ClauseCategory.SAFETY,
            clause_ref="Section IV (HSE) Clause 7.1",
            parameter="Occupational Health & Safety Accreditation",
            threshold="Valid active ISO 45001:2018 certification for Oil & Gas Pipeline Construction",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Active validity required as on date of technical bid opening."
        ),
        TenderRequirement(
            id="REQ-004",
            category=ClauseCategory.TECHNICAL,
            clause_ref="Section V Clause 8.3",
            parameter="Heavy Construction Plant & Machinery Ownership",
            threshold="Possession of minimum 2 Automatic External Pipe Clamps and Induction Bending Rig",
            is_mandatory=False,
            qcbs_weight=20.0,
            description="100% marks for outright ownership; 70% for confirmed non-cancellable lease."
        ),
        TenderRequirement(
            id="REQ-005",
            category=ClauseCategory.FINANCIAL,
            clause_ref="Section II (ITB) Clause 9.1",
            parameter="Earnest Money Deposit (EMD) / Bid Security",
            threshold="INR 25,00,000 via irrevocable Bank Guarantee or MSME statutory exemption",
            is_mandatory=True,
            qcbs_weight=10.0,
            description="BG valid for 180 days from opening date."
        ),
        TenderRequirement(
            id="REQ-006",
            category=ClauseCategory.LEGAL,
            clause_ref="Section II (ITB) Clause 12.4",
            parameter="Non-Blacklisting Affidavit & Integrity Pact",
            threshold="Notarized undertaking on INR 100 stamp paper affirming no debarment by CVC/MoPNG",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Must be signed by authorized signatory with board resolution."
        )
    ]

    boqs = [
        TenderBoQItem(
            item_code="BOQ-01",
            description="Trenching, pipeline stringing, welding 24-inch API 5L X-65 steel pipeline (30 km)",
            unit="Kilometer",
            estimated_quantity=30.0,
            estimated_unit_rate_inr=8500000.0,
            total_estimated_cost_inr=255000000.0
        ),
        TenderBoQItem(
            item_code="BOQ-02",
            description="Horizontal Directional Drilling (HDD) crossing under state highways and riverbed",
            unit="Meter",
            estimated_quantity=1200.0,
            estimated_unit_rate_inr=45000.0,
            total_estimated_cost_inr=54000000.0
        ),
        TenderBoQItem(
            item_code="BOQ-03",
            description="Hydrotesting, pre-commissioning, nitrogen purging and CP cathodic protection",
            unit="Lot",
            estimated_quantity=1.0,
            estimated_unit_rate_inr=18000000.0,
            total_estimated_cost_inr=18000000.0
        )
    ]

    return Tender(
        id="MOPNG-TND-2024-881",
        title="Engineering, Procurement, Construction (EPC) of 30 km High-Pressure Natural Gas Pipeline Network",
        issuing_authority="Ministry of Petroleum and Natural Gas (MoPNG) / GAIL Consortium",
        tender_ref="MoPNG/GAIL/PIPELINE/2024/09",
        estimated_cost_inr=327000000.0,
        emd_amount_inr=2500000.0,
        qcbs_ratio="70:30",
        requirements=reqs,
        boq_items=boqs,
        created_at="2024-09-01"
    )

# ==============================================================================
# 3. MoRTH NATIONAL HIGHWAY EPC TENDER
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
            qcbs_weight=25.0,
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
            category=ClauseCategory.SAFETY,
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
            qcbs_weight=15.0,
            description="Mandatory structural performance guarantee."
        )
    ]

    boqs = [
        TenderBoQItem(
            item_code="BOQ-HW-01",
            description="Earthwork in excavation, embankment construction and subgrade preparation (CBR >= 8%)",
            unit="Cum",
            estimated_quantity=250000.0,
            estimated_unit_rate_inr=280.0,
            total_estimated_cost_inr=70000000.0
        ),
        TenderBoQItem(
            item_code="BOQ-HW-02",
            description="Dense Bituminous Macadam (DBM) with VG-40 Viscosity Grade Bitumen (75mm thickness)",
            unit="Cum",
            estimated_quantity=45000.0,
            estimated_unit_rate_inr=8500.0,
            total_estimated_cost_inr=382500000.0
        ),
        TenderBoQItem(
            item_code="BOQ-HW-03",
            description="Bituminous Concrete (BC) wearing course with polymer modified bitumen (40mm thickness)",
            unit="Cum",
            estimated_quantity=24000.0,
            estimated_unit_rate_inr=11200.0,
            total_estimated_cost_inr=268800000.0
        )
    ]

    return Tender(
        id="MORTH-NH-2024-402",
        title="Construction of 4-Lane Greenfield National Highway Bypass Section (28.4 km) under EPC Mode",
        issuing_authority="Ministry of Road Transport and Highways (MoRTH) / NHAI",
        tender_ref="MoRTH/NHAI/EXP/2024/402",
        estimated_cost_inr=721300000.0,
        emd_amount_inr=5000000.0,
        qcbs_ratio="70:30",
        requirements=reqs,
        boq_items=boqs,
        created_at="2024-09-02"
    )

# ==============================================================================
# 4. BIDDERS DATASET
# ==============================================================================
def get_sample_bidders() -> List[Bidder]:
    b1 = Bidder(
        id="BID-01",
        company_name="L&T Hydrocarbon Engineering Ltd",
        gstin="27AAACL1234F1Z8",
        cin="L99999MH1946PLC004768",
        years_experience=11.5,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=220000000.0,
            turnover_fy22_inr=260000000.0,
            turnover_fy23_inr=255000000.0,
            average_turnover_inr=245000000.0,
            net_worth_inr=850000000.0,
            ca_name="Sharma & Co Chartered Accountants",
            ca_firm="Sharma & Co Chartered Accountants",
            ca_udin="23104588AAAA129481",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="TUV Rheinland", valid_until="2027-05-15", is_active=True, page_number=2),
            Certificate(name="ISO 9001:2015", issuing_body="Bureau Veritas", valid_until="2026-11-20", is_active=True, page_number=2)
        ],
        machinery_owned=["Automatic External Pipe Clamps (4 units)", "Induction Bending Unit 24-inch", "Miller Pipe Welding Stations (12 units)"],
        key_personnel=["Dr. V. Raman (30 yrs exp - Project Director)", "K. Sundaram (Safety Lead, NEBOSH)"],
        boq_quotes=[
            BidderBoQQuote(item_code="BOQ-01", description="Trenching & welding 24-inch API pipeline", quoted_unit_rate_inr=8300000.0, total_quoted_cost_inr=249000000.0),
            BidderBoQQuote(item_code="BOQ-02", description="HDD river crossing", quoted_unit_rate_inr=44000.0, total_quoted_cost_inr=52800000.0),
            BidderBoQQuote(item_code="BOQ-03", description="Hydrotesting & purging", quoted_unit_rate_inr=16200000.0, total_quoted_cost_inr=16200000.0)
        ],
        total_bid_amount_inr=318000000.0,
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder1_LT_Hydrocarbon_Engineering.pdf",
                author="Larsen & Toubro Corporate Secretariat",
                creator="Adobe InDesign 2023 (Windows)",
                producer="Adobe PDF Library 17.0",
                creation_date="2024-09-02T10:15:30Z",
                page_count=2,
                sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            )
        ]
    )

    b2 = Bidder(
        id="BID-02",
        company_name="Apex InfraTech Private Ltd",
        gstin="07AACCA9988G1Z1",
        cin="U45200DL2018PTC334511",
        years_experience=6.0,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=105000000.0,
            turnover_fy22_inr=115000000.0,
            turnover_fy23_inr=116000000.0,
            average_turnover_inr=112000000.0,
            net_worth_inr=45000000.0,
            ca_name="GS & Partners Chartered Accountants",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="Intertek India", valid_until="2022-08-10", is_active=False, page_number=2)
        ],
        machinery_owned=["Manual Pipe Clamps", "Hired Mobile Cranes"],
        key_personnel=["S. Singhania (8 yrs exp)"],
        boq_quotes=[
            BidderBoQQuote(item_code="BOQ-01", description="Trenching & welding 24-inch API pipeline", quoted_unit_rate_inr=7400000.0, total_quoted_cost_inr=222000000.0),
            BidderBoQQuote(item_code="BOQ-02", description="HDD river crossing", quoted_unit_rate_inr=41000.0, total_quoted_cost_inr=49200000.0),
            BidderBoQQuote(item_code="BOQ-03", description="Hydrotesting & purging", quoted_unit_rate_inr=13800000.0, total_quoted_cost_inr=13800000.0)
        ],
        total_bid_amount_inr=285000000.0,
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder2_Apex_InfraTech_Ltd.pdf",
                author="Apex-Workstation-04",
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z",
                page_count=2,
                sha256="c8f18e9064f786968032777ad11832049d5c8ab3f3458ef4feadba00c5c3690d"
            )
        ]
    )

    b3 = Bidder(
        id="BID-03",
        company_name="Zenith Piping & Energy Corp",
        gstin="07AAACZ1122D1Z9",
        cin="U28112DL2019PTC345678",
        years_experience=5.5,
        financial_profile=FinancialProfile(
            turnover_fy21_inr=160000000.0,
            turnover_fy22_inr=175000000.0,
            turnover_fy23_inr=169000000.0,
            average_turnover_inr=168000000.0,
            net_worth_inr=52000000.0,
            ca_name="GS & Partners",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831", # DUPLICATE UDIN matching Bidder 2
            udin_valid=False
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="DNV GL", valid_until="2026-03-30", is_active=True, page_number=2)
        ],
        machinery_owned=["Automatic External Pipe Clamps (2 units)"],
        key_personnel=["R. K. Mehra (12 yrs exp)"],
        boq_quotes=[
            # Front-loaded & Predatory ALT rates
            BidderBoQQuote(item_code="BOQ-01", description="Trenching & welding 24-inch API pipeline", quoted_unit_rate_inr=5100000.0, total_quoted_cost_inr=153000000.0), # -40% predatory
            BidderBoQQuote(item_code="BOQ-02", description="HDD river crossing", quoted_unit_rate_inr=28000.0, total_quoted_cost_inr=33600000.0), # -37% predatory
            BidderBoQQuote(item_code="BOQ-03", description="Hydrotesting & purging", quoted_unit_rate_inr=11400000.0, total_quoted_cost_inr=11400000.0)
        ],
        total_bid_amount_inr=198000000.0, # -39.4% ALT Discount
        documents_metadata=[
            DocumentMetadata(
                filename="Bidder3_Zenith_Piping_Corp.pdf",
                author="Apex-Workstation-04", # IDENTICAL AUTHOR matching Bidder 2
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z", # EXACT SAME SECOND matching Bidder 2
                page_count=2,
                sha256="fa488b0244de82cc78627b46bbdf5888d3e8e19e7555adce7f8dcf62551cf182"
            )
        ]
    )

    return [b1, b2, b3]
