import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("1. Testing Root & Health:")
r = client.get("/health")
assert r.status_code == 200, r.text
print("   Health Status:", r.json()["status"])

print("2. Testing Tenders (MoRTH Highway & Standards Library):")
r_morth = client.get("/api/v1/tenders/morth")
assert r_morth.status_code == 200
print("   MoRTH Tender:", r_morth.json()["id"], "-", r_morth.json()["title"])
print("   Length / Lane-KM:", r_morth.json()["length_km"], "km /", r_morth.json()["lane_km"], "lane-km")
print("   Design Life / Traffic:", r_morth.json()["design_life_years"], "years /", r_morth.json()["design_traffic_msa"], "MSA")

r_std = client.get("/api/v1/tenders/standards")
assert r_std.status_code == 200
print("   Standards Library Count:", len(r_std.json()), "parameters")

print("3. Testing Bidders:")
r_bid = client.get("/api/v1/bidders/sample")
assert r_bid.status_code == 200
print("   Bidders Count:", len(r_bid.json()))
for b in r_bid.json():
    print(f"   - {b['company_name']} (Total Bid: INR {b['total_bid_amount_inr']/1e7:.2f} Cr)")

print("4. Testing Evaluation & Forensics on MoRTH Tender:")
r_eval = client.post("/api/v1/evaluate/run?tender_id=MORTH-NH-2024-402")
assert r_eval.status_code == 200
data_eval = r_eval.json()
print("   Recommended Winner (H1 QCBS):", data_eval["recommended_winner"])
print("   Cartel Alerts Detected:", len(data_eval["cartel_alerts"]))
for alert in data_eval["cartel_alerts"]:
    print(f"     [!] {alert['signal_name']} (Severity: {alert['severity']})")

print("5. Testing OCR Page Image & Bounding Box:")
r_img = client.get("/api/v1/ocr/page-image/Bidder1_LT_Transportation_Infrastructure.pdf/1")
assert r_img.status_code == 200
print("   Rendered PNG Size:", len(r_img.content), "bytes")

r_bbox = client.get("/api/v1/ocr/evidence-bbox?filename=Bidder1_LT_Transportation_Infrastructure.pdf&page_number=1&snippet=turnover")
assert r_bbox.status_code == 200
print("   Evidence Bounding Box:", r_bbox.json()["normalized_bbox"])

print("6. Testing GFR 173 Clarification Notice:")
r_notice = client.get("/api/v1/reports/clarification-notice/MORTH-NH-2024-402/BID-02")
assert r_notice.status_code == 200
print("   Notice Ref:", r_notice.json()["notice_ref"], "| Deficiencies:", r_notice.json()["deficiencies_count"])

print("7. Testing GeM 3.0 / OCDS Export:")
r_gem = client.get("/api/v1/gem/export/MORTH-NH-2024-402")
assert r_gem.status_code == 200
print("   OCDS Release ID:", r_gem.json()["ocds_release_id"])
print("   CVC Clearance Status:", r_gem.json()["cvc_vigilance_clearance_status"])

print("8. Testing IAM Personas & Audit Logging:")
r_users = client.get("/api/v1/iam/users")
assert r_users.status_code == 200
for u in r_users.json():
    print(f"   [User] {u['name']} [{u['role']}] - {u['department']}")

print("\n" + "="*70)
print(">>> ALL 8 MoRTH HIGHWAY INTEGRATION SUITES PASSED 100%! <<<")
print("="*70)
