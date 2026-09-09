from typing import List, Dict, Any
import os
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from app.core.config import settings
from app.models.tender import Tender, TenderRequirement
from app.services.sample_data import get_sample_mopng_tender, get_sample_morth_tender, FULL_GOVERNMENT_CRITERIA_LIBRARY
from app.services.document_parser import DocumentParserService
from app.services.requirement_engine import RequirementEngine

router = APIRouter()
requirement_engine = RequirementEngine()

# In-memory tender store for the session
ACTIVE_TENDERS: Dict[str, Tender] = {}

# Pre-populate with sample tenders
sample_mopng = get_sample_mopng_tender()
sample_morth = get_sample_morth_tender()
ACTIVE_TENDERS[sample_mopng.id] = sample_mopng
ACTIVE_TENDERS[sample_morth.id] = sample_morth

@router.get("/standards", response_model=List[TenderRequirement])
async def get_government_standards_library():
    """Returns the comprehensive 12-criteria CPWD/MoPNG/GeM statutory standards library."""
    return FULL_GOVERNMENT_CRITERIA_LIBRARY

@router.get("/sample", response_model=Tender)
async def get_sample_tender_endpoint():
    """Returns the pre-configured MoPNG sample pipeline tender."""
    return sample_mopng

@router.get("/morth", response_model=Tender)
async def get_sample_morth_endpoint():
    """Returns the pre-configured MoRTH 4-lane Highway EPC sample tender."""
    return sample_morth

@router.get("/{tender_id}", response_model=Tender)
async def get_tender_by_id(tender_id: str):
    if tender_id not in ACTIVE_TENDERS:
        raise HTTPException(status_code=404, detail="Tender not found")
    return ACTIVE_TENDERS[tender_id]

@router.post("/{tender_id}/thresholds", response_model=Tender)
async def update_tender_thresholds(tender_id: str, updated_requirements: List[TenderRequirement] = Body(...)):
    """Executive threshold tuner: Updates requirements and thresholds with validation against minimum statutory government floors."""
    if tender_id not in ACTIVE_TENDERS:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    # Statutory validation: Mandatory eligibility criteria cannot be disabled
    for req in updated_requirements:
        if req.id in ["STD-01", "REQ-001", "REQ-MORTH-01"] and not req.is_mandatory:
            raise HTTPException(
                status_code=400,
                detail="Violation of GFR Rule 173: Minimum Annual Turnover requirement cannot be marked non-mandatory."
            )
        if req.id in ["STD-06", "REQ-005", "REQ-MORTH-05"] and not req.is_mandatory:
            raise HTTPException(
                status_code=400,
                detail="Violation of CVC Guidelines: Earnest Money Deposit (EMD) is legally mandatory for all non-MSME bids."
            )

    tender = ACTIVE_TENDERS[tender_id]
    tender.requirements = updated_requirements
    ACTIVE_TENDERS[tender_id] = tender
    return tender

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

