# SIH26100: AI-Powered Bid Compliance & Procurement Intelligence System

**Organization:** Ministry of Petroleum and Natural Gas (MoPNG) / Compatible with MoRTH, GeM, and CPPP  
**Problem Statement ID:** SIH26100  
**Theme:** Smart Governance, Anti-Corruption, Quality Infrastructure Procurement

---

## 📌 Executive Summary

Every year, Indian government ministries (MoPNG, MoRTH, NHAI, ONGC, GAIL) publish thousands of public tenders. For each tender, dozens of EPC contractors submit **1,500–5,000 pages of scanned PDFs** (balance sheets, CA certificates with UDINs, past completion certificates, joint venture deeds, machinery lists, ISO accreditations). 

Tender Evaluation Committees (TECs) take **45 to 90 days** manually verifying compliance matrices in Excel. This creates two fatal vulnerabilities:
1. **The L1 Trap (Pothole Syndrome):** Technical evaluation is treated as a flat binary gate (Pass/Fail). Substandard contractors who barely pass technical scrutiny quote **35% below realistic engineering estimates**, win L1, cut bitumen/welding quality, or delay projects with dispute claims.
2. **Cartelization & Document Forgery:** Rival bidders secretly collude from the same office, reuse Chartered Accountant UDIN numbers, or submit forged accreditations.

This system is an **End-to-End Autonomous Procurement Intelligence Platform** that extracts tender rules, cross-verifies bidder evidence down to exact page numbers, exposes cartel metadata, and ranks bidders using **Risk-Adjusted QCBS (Quality & Cost Based Selection)**.

---

## 🏗️ Architecture: High-Level & Low-Level Design

### High-Level Design (HLD)
```
Tender RFP (PDF) ───► [ Document Parser & OCR ] ───► [ Requirement Engine ]
                                                              │ (Structured JSON)
Bidder Dossiers ────► [ Document Parser & OCR ]               ▼
                                │               [ Hybrid RAG & Verification Engine ]
                                ▼                             │
                    [ Forensics & Cartel Engine ]             ▼
                                │               [ QCBS & ALT Risk Scoring Engine ]
                                ▼                             │
                    [ Central Vigilance Alerts ]              ▼
                                └───────────────► [ Non-Tech-Savvy Web Portal ]
```

### Low-Level Design (LLD)
```
bidder/
├── backend/
│   ├── .env                    # Groq & Gemini API keys from NyaAi
│   ├── requirements.txt        # FastAPI, PyMuPDF, Pydantic, Groq, Google-GenAI
│   ├── main.py                 # FastAPI app, CORS, routers
│   └── app/
│       ├── core/config.py      # App configurations & settings
│       ├── models/             # Pydantic schemas (Tender, Bidder, Compliance, Report)
│       ├── services/
│       │   ├── document_parser.py    # PyMuPDF text & PDF metadata extractor
│       │   ├── requirement_engine.py # Groq Llama-3.3-70b / Gemini requirement extraction
│       │   ├── compliance_engine.py  # Clause-to-evidence cross-matcher & proof generator
│       │   ├── forensics_engine.py   # Cartel detection, identical author check, UDIN audit
│       │   ├── scoring_engine.py     # GFR 2017 QCBS + ALT (Abnormally Low Tender) detector
│       │   └── sample_data.py        # Authentic MoPNG 30 km Pipeline EPC tender & 3 bidders
│       └── api/v1/             # REST Endpoints: /tenders, /bidders, /evaluate, /reports
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # 3-Step Wizard for Government Evaluators
│   │   ├── index.css           # Clean Government of India / MoPNG portal theme
│   │   └── main.jsx
├── run_backend.bat             # 1-Click launcher for Backend
├── run_frontend.bat            # 1-Click launcher for Frontend
└── README.md
```

---

## 🚀 How to Run the Project

### Option A: Quick Launch via Batch Files (Recommended)
1. Double-click **`run_backend.bat`** (Starts FastAPI server at `http://localhost:8000`).
2. Double-click **`run_frontend.bat`** (Starts React portal at `http://localhost:5173`).
3. Open `http://localhost:5173` in your browser.

### Option B: Manual Terminal Execution
```bash
# Terminal 1: Backend
cd backend
..\venv\Scripts\activate
uvicorn main:app --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 💡 Key Innovations That Win SIH

1. **Digital Forensics & Anti-Cartelization Banner**:
   - In our pre-loaded test case, **Apex InfraTech** and **Zenith Piping** are competing bidders.
   - The AI forensic engine examines raw PDF metadata, detecting that both submissions were exported by the exact same author environment (`Apex-Workstation-04`) at the identical second, and shared a duplicate Chartered Accountant UDIN (`23049182BBBB912831`).
   - Flags an immediate **Critical Cartel Alert** under Section 3 of the Competition Act.

2. **The MoPNG Infrastructure Safety Shield (Abnormally Low Tender Detection)**:
   - Evaluates whether a bidder quoted $>20\%$ below the engineering estimate.
   - Flags *Zenith Piping* for quoting 39.4% below benchmark (₹19.80 Cr vs ₹32.70 Cr estimate).
   - Automatically computes a 5-year **Life-Cycle Risk Penalty** for anticipated maintenance and dispute claims.

3. **100% Explainable Grounding (Side-by-Side Dual Audit Proof)**:
   - Reviewers can click **"View Proof"** on any requirement.
   - Displays the exact Tender Condition on the left alongside the verified quote, document filename, and page number from the bidder submission on the right.
   - Eliminates hallucination risk; empowers human officers to sign off with total confidence.

4. **1-Click Official TEC Report**:
   - Generates a formatted Government Tender Evaluation Committee (TEC) Scrutiny Note ready to be attached to official procurement files.
