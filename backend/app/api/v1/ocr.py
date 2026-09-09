from fastapi import APIRouter, HTTPException, Response, Query
from app.services.ocr_pipeline import OCRPipelineService

router = APIRouter()

@router.get("/page-image/{filename}/{page_number}")
async def get_page_image(filename: str, page_number: int):
    """Renders and streams a specific PDF page as a high-resolution PNG image."""
    img_bytes = OCRPipelineService.render_page_image(filename, page_number)
    if not img_bytes:
        raise HTTPException(status_code=404, detail=f"Page {page_number} of {filename} could not be rendered")
    
    return Response(content=img_bytes, media_type="image/png")

@router.get("/evidence-bbox")
async def get_evidence_bounding_box(
    filename: str = Query(...),
    page_number: int = Query(1),
    snippet: str = Query(...)
):
    """Returns the normalized percentage bounding box [x, y, width, height] for evidence highlighting."""
    bbox = OCRPipelineService.find_evidence_bbox(filename, snippet, page_number)
    page_info = OCRPipelineService.extract_page_lines_with_bbox(filename, page_number)
    return {
        "filename": filename,
        "page_number": page_number,
        "normalized_bbox": bbox, # [x_pct, y_pct, w_pct, h_pct]
        "page_dimensions": {"width": page_info["width"], "height": page_info["height"]}
    }
