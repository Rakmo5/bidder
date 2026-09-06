from app.models.tender import Tender, TenderRequirement, TenderBoQItem, ClauseCategory
from app.models.bidder import Bidder, FinancialProfile, Certificate, BidderBoQQuote, DocumentMetadata

def get_sample_mopng_tender() -> Tender:
    reqs = [
        TenderRequirement(
            id="REQ-001",
            category=ClauseCategory.ELIGIBILITY,
            clause_ref="Section III (SCC) Clause 3.2",
            parameter="Minimum Average Annual Turnover",
            threshold="₹15.00 Crore minimum over last 3 audited financial years (FY 2020-21, 2021-22, 2022-23)",
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
            threshold="₹25,00,000 via irrevocable Bank Guarantee or MSME statutory exemption",
            is_mandatory=True,
            qcbs_weight=10.0,
            description="BG valid for 180 days from opening date."
        ),
        TenderRequirement(
            id="REQ-006",
            category=ClauseCategory.LEGAL,
            clause_ref="Section II (ITB) Clause 12.4",
            parameter="Non-Blacklisting Affidavit & Integrity Pact",
            threshold="Notarized undertaking on ₹100 stamp paper affirming no debarment by CVC/MoPNG",
            is_mandatory=True,
            qcbs_weight=15.0,
            description="Must be signed by authorized signatory with board resolution."
        )
    ]

    boqs = [
        TenderBoQItem(
            item_code="BOQ-01",
            description="Trenching, pipeline stringing, welding and laying of 24-inch API 5L X-65 steel pipeline (30 km)",
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
        estimated_cost_inr=327000000.0, # ₹32.70 Crore
        emd_amount_inr=2500000.0,       # ₹25 Lakhs
        qcbs_ratio="70:30",
        requirements=reqs,
        boq_items=boqs,
        created_at="2024-09-01"
    )

def get_sample_bidders() -> list[Bidder]:
    # Bidder 1: Larsen & Toubro Hydrocarbon (Pristine, Fully Compliant)
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
            average_turnover_inr=245000000.0, # ₹24.5 Cr
            net_worth_inr=850000000.0,
            ca_name="Rajesh Sharma & Associates",
            ca_firm="Sharma & Co Chartered Accountants",
            ca_udin="23104588AAAA129481",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="TUV Rheinland", valid_until="2027-05-15", is_active=True, page_number=3),
            Certificate(name="ISO 9001:2015", issuing_body="Bureau Veritas", valid_until="2026-11-20", is_active=True, page_number=5)
        ],
        machinery_owned=["Automatic External Pipe Clamps (4 units)", "Induction Bending Unit 24-inch", "Miller Pipe Welding Stations (12 units)"],
        key_personnel=["Dr. V. Raman (30 yrs exp - Project Director)", "K. Sundaram (Safety Lead, NEBOSH)"],
        total_bid_amount_inr=318000000.0, # ₹31.80 Cr (Viable quote, -2.7% of estimate)
        documents_metadata=[
            DocumentMetadata(
                filename="LTHL_Technical_Bid_Final.pdf",
                author="Larsen & Toubro Corporate Secretariat",
                creator="Adobe InDesign 2023 (Windows)",
                producer="Adobe PDF Library 17.0",
                creation_date="2024-09-02T10:15:30Z",
                page_count=182,
                sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            )
        ]
    )

    # Bidder 2: Apex InfraTech Ltd (Deficient: Fails Turnover & Expired ISO)
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
            average_turnover_inr=112000000.0, # ₹11.2 Cr (FAILS ₹15 Cr requirement)
            net_worth_inr=45000000.0,
            ca_name="Gupta & Singhal Associates",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831",
            udin_valid=True
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="Intertek India", valid_until="2022-08-10", is_active=False, page_number=2) # EXPIRED
        ],
        machinery_owned=["Manual Pipe Clamps", "Hired Mobile Cranes"],
        key_personnel=["S. Singhania (8 yrs exp)"],
        total_bid_amount_inr=285000000.0, # ₹28.5 Cr
        documents_metadata=[
            DocumentMetadata(
                filename="Apex_Infra_Tender_Submission.pdf",
                author="Apex-Workstation-04",
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z",
                page_count=64,
                sha256="c8f18e9064f786968032777ad11832049d5c8ab3f3458ef4feadba00c5c3690d"
            )
        ]
    )

    # Bidder 3: Zenith Piping Corp (Cartelized with Apex + Abnormally Low Tender / ALT)
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
            average_turnover_inr=168000000.0, # ₹16.8 Cr (Passes)
            net_worth_inr=52000000.0,
            ca_name="GS & Partners",
            ca_firm="GS & Partners",
            ca_udin="23049182BBBB912831", # DUPLICATE UDIN matching Bidder 2!
            udin_valid=False
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="DNV GL", valid_until="2026-03-30", is_active=True, page_number=4)
        ],
        machinery_owned=["Automatic External Pipe Clamps (2 units)"],
        key_personnel=["R. K. Mehra (12 yrs exp)"],
        total_bid_amount_inr=198000000.0, # ₹19.8 Cr (-39.4% discount! ALT Trigger)
        documents_metadata=[
            DocumentMetadata(
                filename="Zenith_Pipeline_Proposal.pdf",
                author="Apex-Workstation-04", # IDENTICAL author matching Bidder 2!
                creator="Quartz PDFContext / macOS 14.1",
                producer="macOS 14.1 Quartz PDFContext",
                creation_date="2024-09-03T16:22:10Z", # EXACT SAME SECOND as Bidder 2!
                page_count=71,
                sha256="fa488b0244de82cc78627b46bbdf5888d3e8e19e7555adce7f8dcf62551cf182"
            )
        ]
    )

    return [b1, b2, b3]
