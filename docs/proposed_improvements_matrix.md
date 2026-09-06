# SIH26100: Proposed System Improvements & Feature Status Matrix

This matrix tracks the 5 strategic improvements for the **AI-Powered Bid Compliance & Procurement Intelligence System (SIH26100)**, categorized by implementation simplicity and current status.

---

## 📊 Feature Status & Simplicity Matrix

| # | Improvement / Feature | Target Module | Technical Simplicity | Current Status | Impact on SIH Evaluators / Ministry |
| :-: | :--- | :--- | :-: | :-: | :--- |
| **1** | **Multi-Ministry Domain Switcher**<br>*(MoPNG Hydrocarbon Pipeline vs. MoRTH 4-Lane Highway)* | Backend `sample_data.py` & Frontend `App.jsx` | **Simple**<br>*(Config & Data preset)* | ⏳ **Pending** | **10/10** — Demonstrates domain versatility. Shows how the system addresses road-contractor underbidding, bitumen adulteration, and premature potholing. |
| **2** | **Direct Drag-and-Drop PDF Upload in UI**<br>*(Live PDF ingestion with upload progress & OCR trigger)* | Frontend `App.jsx` & Backend `/upload` | **Simple**<br>*(Native HTML5 drag-drop + FormData)* | ⏳ **Pending** | **9/10** — Allows judges to drop any public PDF live from [etenders.gov.in](https://etenders.gov.in) and watch it extract rules on stage. |
| **3** | **Visual Collusion Network Graph**<br>*(Interactive Node-Link diagram linking cartelized bidders to shared machines, UDINs & IPs)* | Frontend Component (Interactive SVG / Canvas) | **Moderate**<br>*(SVG node layout + dynamic links)* | ⏳ **Pending** | **10/10** — Immediate "intelligence agency" visual appeal. Non-technical officers instantly grasp who is colluding with whom. |
| **4** | **Itemized BoQ Rate Analyzer**<br>*(Line-by-line rate comparison against CPWD/MoRTH DSR benchmark to catch front-loading & underbidding)* | Backend `scoring_engine.py` & Frontend Table | **Moderate**<br>*(Line-item variance formula)* | ⏳ **Pending** | **9.5/10** — Stops contractors from quoting 200% on earthwork to extract cash early and -40% on finishing works. |
| **5** | **GFR Rule 173 Clarification Dispatcher**<br>*(1-Click formal 48-hour clarification notice drafting with pre-filled clause citations)* | Backend `reports.py` & Frontend Modal | **Simple**<br>*(Template generation + export)* | ⏳ **Pending** | **8.5/10** — Shows deep grounding in Indian procurement law; gives Tender Committees a legal mechanism before outright rejection. |

---

## 🛠️ Detailed Breakdown of Each Improvement

### 1. Multi-Ministry Domain Switcher (MoPNG vs MoRTH)
* **What it does:** Allows the user to toggle between two real-world infrastructure tenders:
  * **MoPNG Mode:** Gas Pipeline EPC (API 5L X-65 steel pipes, ISO 45001 safety, Horizontal Directional Drilling, hydrotesting).
  * **MoRTH Mode:** NHAI 4-Lane Highway Construction (VG-40 Bitumen grade, Electronic sensor pavers, Road safety audit, 5-year Defect Liability Period).
* **Simplicity Level:** **Simple** (Requires adding the MoRTH dataset to `sample_data.py` and a dropdown toggle in `App.jsx`).

### 2. Direct Drag-and-Drop File Upload in UI
* **What it does:** Replaces or complements the 1-click sample buttons with an intuitive dropzone where users can upload any custom tender RFP or bidder PDF.
* **Simplicity Level:** **Simple** (The FastAPI backend endpoints `/api/v1/tenders/upload` and `/api/v1/bidders/upload` are already implemented; only the UI drag-and-drop state needs wiring).

### 3. Visual Collusion Network Graph
* **What it does:** Draws an interactive graph when cartel signals are flagged:
  * Red circle nodes for `Apex InfraTech` and `Zenith Piping`.
  * Yellow diamond nodes for `Machine: Apex-Workstation-04`, `Shared UDIN: 23049182BBBB912831`, and `Timestamp: 16:22:10Z`.
  * Connecting lines indicating the exact digital forensics evidence.
* **Simplicity Level:** **Moderate** (Built using clean inline SVG or a lightweight canvas component with zero external heavy libraries).

### 4. Itemized BoQ Deep-Dive (Front-Loading & Unbalanced Bids)
* **What it does:** Scans the Bill of Quantities table line-by-line:
  * Compares contractor quoted unit rates against the official Schedule of Rates (SOR).
  * Flags front-loaded items (inflated mobilization rates) and predatory underquoted items (bitumen/welding quoted $< 30\%$ of cost).
* **Simplicity Level:** **Moderate** (Requires calculating line-item percentage variances and rendering an itemized BoQ table).

### 5. GFR Rule 173 Clarification Notice Generator
* **What it does:** Under General Financial Rules (GFR) 2017 Rule 173, if an otherwise qualified bidder has a minor clerical defect (e.g. illegible notary stamp or missing appendix page), the committee can issue a time-bound clarification query.
* **Simplicity Level:** **Simple** (A "Draft Clarification Letter" button that generates an official notification template citing the exact clause and discrepancy).
