from typing import Dict, Any
from app.ai_engine.pipeline.requirement_extractor import RequirementExtractor

class RequirementEngine:
    """Service facade delegating tender requirement extraction to the modular ai_engine package."""
    
    def __init__(self):
        self._extractor = RequirementExtractor()

    def extract_requirements(self, tender_text: str) -> Dict[str, Any]:
        return self._extractor.extract_from_text(tender_text)
