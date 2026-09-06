import os
import shutil
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.config import settings
from app.models.bidder import Bidder, FinancialProfile, Certificate
from app.services.sample_data import get_sample_bidders
from app.services.document_parser import DocumentParserService

router = APIRouter()

ACTIVE_BIDDERS = {}

# Pre-populate sample bidders
for b in get_sample_bidders():
    ACTIVE_BIDDERS[b.id] = b

@router.get("/sample", response_model=List[Bidder])
async def get_sample_bidders_endpoint():
    """Returns the 3 pre-configured realistic bidder profiles."""
    return get_sample_bidders()

@router.get("/all", response_model=List[Bidder])
async def get_all_bidders():
    return list(ACTIVE_BIDDERS.values())

@router.get("/{bidder_id}", response_model=Bidder)
async def get_bidder_by_id(bidder_id: str):
    if bidder_id not in ACTIVE_BIDDERS:
        raise HTTPException(status_code=404, detail="Bidder not found")
    return ACTIVE_BIDDERS[bidder_id]

@router.post("/upload", response_model=Bidder)
async def upload_bidder_document(
    company_name: str = Form(...),
    quoted_price_inr: float = Form(...),
    years_experience: float = Form(5.0),
    turnover_inr: float = Form(200000000.0),
    ca_udin: str = Form(""),
    file: UploadFile = File(...)
):
    bidder_id = f"BID-{uuid.uuid4().hex[:6].upper()}"
    save_path = settings.UPLOAD_DIR / f"{bidder_id}_{file.filename}"
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    full_text, metadata = DocumentParserService.extract_full_text(save_path)

    new_bidder = Bidder(
        id=bidder_id,
        company_name=company_name,
        years_experience=years_experience,
        financial_profile=FinancialProfile(
            average_turnover_inr=turnover_inr,
            ca_udin=ca_udin,
            udin_valid=bool(ca_udin)
        ),
        certificates=[
            Certificate(name="ISO 45001:2018", issuing_body="Audited Body", is_active=True, page_number=1)
        ],
        total_bid_amount_inr=quoted_price_inr,
        documents_metadata=[metadata],
        raw_text=full_text[:5000]
    )

    ACTIVE_BIDDERS[bidder_id] = new_bidder
    return new_bidder
