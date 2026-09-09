import io
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
try:
    import pymupdf as fitz
except ImportError:
    import fitz

from app.core.config import settings

DEMO_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "demo_pdfs"
DEMO_DIR_ALT = Path(__file__).resolve().parent.parent.parent / "data" / "demo_pdfs"
UPLOAD_DIR = settings.UPLOAD_DIR

class OCRPipelineService:
    @staticmethod
    def _find_file(filename: str) -> Optional[Path]:
        # Check uploads dir first, then demo dirs
        search_dirs = [UPLOAD_DIR, DEMO_DIR, DEMO_DIR_ALT]
        for d in search_dirs:
            if d.exists():
                direct = d / filename
                if direct.exists():
                    return direct
        # Partial match
        for d in search_dirs:
            if d.exists():
                for f in d.glob(f"*{filename}*"):
                    if f.is_file():
                        return f
        return None


    @classmethod
    def render_page_image(cls, filename: str, page_number: int = 1) -> Optional[bytes]:
        file_path = cls._find_file(filename)
        if not file_path or not file_path.exists():
            return None

        try:
            doc = fitz.open(str(file_path))
            if page_number < 1 or page_number > len(doc):
                page_number = 1
            page = doc[page_number - 1]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            doc.close()
            return img_bytes
        except Exception:
            return None

    @classmethod
    def extract_page_lines_with_bbox(cls, filename: str, page_number: int = 1) -> Dict[str, Any]:
        file_path = cls._find_file(filename)
        if not file_path or not file_path.exists():
            return {"page": page_number, "width": 612, "height": 792, "lines": []}

        try:
            doc = fitz.open(str(file_path))
            if page_number < 1 or page_number > len(doc):
                page_number = 1
            page = doc[page_number - 1]
            rect = page.rect
            width, height = rect.width, rect.height

            # Extract blocks
            text_blocks = page.get_text("blocks")
            lines = []
            for b in text_blocks:
                x0, y0, x1, y1, text, block_no, block_type = b[:7]
                if text.strip():
                    lines.append({
                        "text": text.strip(),
                        "bbox": [x0, y0, x1, y1],
                        "normalized_bbox": [
                            round((x0 / width) * 100, 2),
                            round((y0 / height) * 100, 2),
                            round(((x1 - x0) / width) * 100, 2),
                            round(((y1 - y0) / height) * 100, 2)
                        ]
                    })
            doc.close()
            return {"page": page_number, "width": width, "height": height, "lines": lines}
        except Exception:
            return {"page": page_number, "width": 612, "height": 792, "lines": []}

    @classmethod
    def find_evidence_bbox(cls, filename: str, snippet: str, page_number: int = 1) -> Optional[List[float]]:
        """Returns normalized [x_pct, y_pct, width_pct, height_pct] matching the evidence snippet."""
        page_info = cls.extract_page_lines_with_bbox(filename, page_number)
        lines = page_info.get("lines", [])
        if not lines:
            return [10.0, 30.0, 80.0, 15.0] # Default fallback box

        # Find best matching line by token overlap
        words = set([w.lower().strip(".,;:\"'()") for w in snippet.split() if len(w) > 3])
        best_match = None
        highest_overlap = 0

        for line in lines:
            line_text = line["text"].lower()
            overlap = sum(1 for w in words if w in line_text)
            if overlap > highest_overlap:
                highest_overlap = overlap
                best_match = line["normalized_bbox"]

        if best_match and highest_overlap > 0:
            return best_match
        return [8.0, 25.0, 84.0, 20.0]
