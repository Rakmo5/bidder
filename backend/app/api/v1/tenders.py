import os
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.models.tender import Tender
from app.services.sample_data import get_sample_mopng_tender
from app.services.document_parser import DocumentParserService
from app.services.requirement_engine import RequirementEngine

router = APIRouter()
requirement_engine = RequirementEngine()

# In-memory tender store for the session
ACTIVE_TENDERS = {}

# Pre-populate with sample tender
sample_tender = get_sample_mopng_tender()
ACTIVE_TENDERS[sample_tender.id] = sample_tender

@router.get("/sample", response_model=Tender)
async def get_sample_tender_endpoint():
    """Returns the pre-configured MoPNG sample pipeline tender."""
    return sample_tender

@router.get("/{tender_id}", response_model=Tender)
async def get_tender_by_id(tender_id: str):
    if tender_id not in ACTIVE_TENDERS:
        raise HTTPException(status_code=404, detail="Tender not found")
    return ACTIVE_TENDERS[tender_id]

@router.post("/upload", response_model=Tender)
async def upload_tender_file(file: UploadFile = File(...)):
    """Uploads a tender PDF, extracts requirements and BoQ items via AI."""
    tender_id = f"TND-{uuid.uuid4().hex[:8].upper()}"
    save_path = settings.UPLOAD_DIR / f"{tender_id}_{file.filename}"
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    full_text, metadata = DocumentParserService.extract_full_text(save_path)
    
    # Extract requirements via LLM
    extracted = requirement_engine.extract_requirements(full_text)
    
    new_tender = Tender(
        id=tender_id,
        title=file.filename.replace(".pdf", "").replace("_", " ").title(),
        issuing_authority="Public Procurement Authority",
        tender_ref=f"TND/{tender_id}",
        estimated_cost_inr=50000000.0, # Default or parsed
        emd_amount_inr=1000000.0,
        qcbs_ratio="70:30",
        requirements=extracted.get("requirements", []),
        boq_items=extracted.get("boq_items", []),
        created_at="2024-09-04"
    )

    ACTIVE_TENDERS[tender_id] = new_tender
    return new_tender
