import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("1. Testing Root & Health:")
r = client.get("/health")
assert r.status_code == 200, r.text
print("   Health Status:", r.json()["status"])

print("2. Testing Tenders (MoPNG & MoRTH & Standards):")
r_mopng = client.get("/api/v1/tenders/sample")
assert r_mopng.status_code == 200
print("   MoPNG Tender:", r_mopng.json()["id"], "-", r_mopng.json()["title"])

r_morth = client.get("/api/v1/tenders/morth")
assert r_morth.status_code == 200
print("   MoRTH Tender:", r_morth.json()["id"], "-", r_morth.json()["title"])

r_std = client.get("/api/v1/tenders/standards")
assert r_std.status_code == 200
print("   Standards Library Count:", len(r_std.json()), "parameters")

print("3. Testing Bidders:")
r_bid = client.get("/api/v1/bidders/sample")
assert r_bid.status_code == 200
print("   Bidders Count:", len(r_bid.json()))

print("4. Testing Evaluation & Forensics:")
r_eval = client.post("/api/v1/evaluate/run?tender_id=MOPNG-TND-2024-881")
assert r_eval.status_code == 200
data_eval = r_eval.json()
print("   Leaderboard Rank 1:", data_eval["leaderboard"][0]["company_name"])
print("   Cartel Alerts Detected:", len(data_eval["cartel_alerts"]))

print("5. Testing OCR Page Image & Bounding Box:")
r_img = client.get("/api/v1/ocr/page-image/Bidder1_LT_Hydrocarbon_Engineering.pdf/1")
assert r_img.status_code == 200
print("   Rendered PNG Size:", len(r_img.content), "bytes")

r_bbox = client.get("/api/v1/ocr/evidence-bbox?filename=Bidder1_LT_Hydrocarbon_Engineering.pdf&page_number=1&snippet=turnover")
assert r_bbox.status_code == 200
print("   Evidence Bounding Box:", r_bbox.json()["normalized_bbox"])

print("6. Testing GFR 173 Clarification Notice:")
r_notice = client.get("/api/v1/reports/clarification-notice/MOPNG-TND-2024-881/BID-02")
assert r_notice.status_code == 200
print("   Notice Ref:", r_notice.json()["notice_ref"], "| Deficiencies:", r_notice.json()["deficiencies_count"])

print("7. Testing GeM 3.0 / OCDS Export:")
r_gem = client.get("/api/v1/gem/export/MOPNG-TND-2024-881")
assert r_gem.status_code == 200
print("   OCDS Release ID:", r_gem.json()["ocds_release_id"])
print("   CVC Clearance Status:", r_gem.json()["cvc_vigilance_clearance_status"])

print("8. Testing IAM Personas & Audit Logging:")
r_users = client.get("/api/v1/iam/users")
assert r_users.status_code == 200
for u in r_users.json():
    print(f"   [User] {u['name']} [{u['role']}] - {u['department']}")

print("9. Testing AI & Hybrid RAG Retrieval Engine:")
r_rag_status = client.get("/api/v1/ai/status")
assert r_rag_status.status_code == 200
print("   RAG Pipeline Architecture:", r_rag_status.json()["pipeline_architecture"])

r_rag_query = client.post("/api/v1/ai/query-rag", json={
    "document_name": "Bidder1_LT_Hydrocarbon_Engineering.pdf",
    "query": "What is the average 3-year turnover and the ICAI UDIN number?"
})
assert r_rag_query.status_code == 200
rag_data = r_rag_query.json()
print("   RAG Grounded Answer:", rag_data["answer"])
print("   RAG Confidence Score:", f"{rag_data['confidence_score']*100:.1f}%")
print("   RAG Provider Used:", rag_data["llm_provider_used"])

print("\n" + "="*70)
print(">>> ALL 9 ENTERPRISE AI & RAG SYSTEM INTEGRATION TESTS PASSED 100%! <<<")
print("="*70)

