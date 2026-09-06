import os
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import pypdf
try:
    import pymupdf as fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    try:
        import fitz
        HAS_PYMUPDF = True
    except ImportError:
        HAS_PYMUPDF = False

from app.models.bidder import DocumentMetadata

class DocumentParserService:
    @staticmethod
    def calculate_sha256(file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def extract_metadata(cls, file_path: Path) -> DocumentMetadata:
        filename = file_path.name
        sha256 = cls.calculate_sha256(file_path)
        
        author = "Unknown"
        creator = "Unknown"
        producer = "Unknown"
        creation_date = None
        mod_date = None
        page_count = 1

        if HAS_PYMUPDF:
            try:
                doc = fitz.open(str(file_path))
                page_count = len(doc)
                meta = doc.metadata or {}
                author = meta.get("author") or "Unknown"
                creator = meta.get("creator") or "Unknown"
                producer = meta.get("producer") or "Unknown"
                creation_date = meta.get("creationDate")
                mod_date = meta.get("modDate")
                doc.close()
            except Exception as e:
                pass
        else:
            try:
                reader = pypdf.PdfReader(str(file_path))
                page_count = len(reader.pages)
                meta = reader.metadata or {}
                author = meta.get("/Author", "Unknown")
                creator = meta.get("/Creator", "Unknown")
                producer = meta.get("/Producer", "Unknown")
                creation_date = meta.get("/CreationDate")
                mod_date = meta.get("/ModDate")
            except Exception as e:
                pass

        return DocumentMetadata(
            filename=filename,
            author=author or "Unknown",
            creator=creator or "Unknown",
            producer=producer or "Unknown",
            creation_date=str(creation_date) if creation_date else None,
            mod_date=str(mod_date) if mod_date else None,
            page_count=page_count,
            sha256=sha256
        )

    @classmethod
    def extract_pages(cls, file_path: Path) -> List[Dict[str, Any]]:
        """Extracts text page-by-page to retain grounding/page references."""
        pages_content = []
        if HAS_PYMUPDF:
            try:
                doc = fitz.open(str(file_path))
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text("text")
                    pages_content.append({
                        "page_number": page_num,
                        "text": text.strip()
                    })
                doc.close()
                return pages_content
            except Exception as e:
                pass

        # Fallback to PyPDF
        try:
            reader = pypdf.PdfReader(str(file_path))
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                pages_content.append({
                    "page_number": page_num,
                    "text": text.strip()
                })
        except Exception as e:
            pass

        return pages_content

    @classmethod
    def extract_full_text(cls, file_path: Path) -> Tuple[str, DocumentMetadata]:
        meta = cls.extract_metadata(file_path)
        pages = cls.extract_pages(file_path)
        full_text = "\n\n--- PAGE BREAK ---\n\n".join([f"[Page {p['page_number']}]\n{p['text']}" for p in pages])
        return full_text, meta
