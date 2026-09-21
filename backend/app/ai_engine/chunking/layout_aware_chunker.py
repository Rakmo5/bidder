from pathlib import Path
from typing import List
try:
    import pymupdf as fitz
except ImportError:
    import fitz

from app.ai_engine.chunking.base_chunker import BaseChunker, DocumentChunk

class LayoutAwarePDFChunker(BaseChunker):
    """
    Layout-aware PDF Chunker using PyMuPDF.
    Extracts atomic text blocks, computing exact bounding boxes normalized to page dimensions.
    """
    
    def chunk_file(self, file_path: Path) -> List[DocumentChunk]:
        if not file_path.exists():
            return []

        doc_name = file_path.name
        doc = fitz.open(str(file_path))
        chunks: List[DocumentChunk] = []
        chunk_idx = 0

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            rect = page.rect
            width, height = rect.width, rect.height
            blocks = page.get_text("blocks")

            for b in blocks:
                x0, y0, x1, y1, text, block_no, block_type = b[:7]
                clean_text = " ".join(text.strip().split())
                if len(clean_text) < 15:
                    continue

                chunk_id = f"{doc_name}_p{page_idx+1}_c{chunk_idx}"
                norm_bbox = [
                    round((x0 / width) * 100, 2),
                    round((y0 / height) * 100, 2),
                    round(((x1 - x0) / width) * 100, 2),
                    round(((y1 - y0) / height) * 100, 2)
                ]

                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_name=doc_name,
                    page_number=page_idx + 1,
                    text=clean_text,
                    normalized_bbox=norm_bbox,
                    tokens_count=len(clean_text.split())
                )
                chunks.append(chunk)
                chunk_idx += 1

        doc.close()
        return chunks
