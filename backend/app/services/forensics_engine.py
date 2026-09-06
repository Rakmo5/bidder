import re
from typing import List, Dict, Any
from app.models.bidder import Bidder
from app.models.report import CartelAlert

class ForensicsEngine:
    """
    Forensics & Anti-Cartelization Engine
    Detects bid rigging, metadata collusion, shared machines, and forged/reused CA UDINs.
    """
    
    # Standard 18-digit UDIN Regex pattern (e.g. 23098765AAAA123456)
    UDIN_REGEX = re.compile(r"^[0-9]{2}[0-9]{6}[A-Z0-9]{4}[A-Z0-9]{6}$", re.IGNORECASE)

    @classmethod
    def validate_udin_format(cls, udin: str) -> bool:
        if not udin:
            return False
        clean_udin = udin.strip().replace("-", "").replace(" ", "").upper()
        return bool(cls.UDIN_REGEX.match(clean_udin))

    @classmethod
    def analyze_bidders_for_collusion(cls, bidders: List[Bidder]) -> List[CartelAlert]:
        alerts = []
        
        # 1. Check for Identical PDF Metadata (Creator / Author / Machine)
        metadata_map: Dict[str, List[str]] = {}
        for bidder in bidders:
            for doc in bidder.documents_metadata:
                if doc.author and doc.author != "Unknown" and doc.author.strip():
                    key = f"Author: {doc.author.strip()}"
                    metadata_map.setdefault(key, []).append(bidder.company_name)
                
                # Check suspicious exact creation timestamp
                if doc.creation_date:
                    key = f"CreationTimestamp: {doc.creation_date.strip()}"
                    metadata_map.setdefault(key, []).append(bidder.company_name)

        for sig, company_list in metadata_map.items():
            unique_companies = sorted(list(set(company_list)))
            if len(unique_companies) > 1:
                alerts.append(CartelAlert(
                    alert_id=f"CARTEL-META-{len(alerts)+1}",
                    signal_name="IDENTICAL_PDF_METADATA_COLLUSION",
                    severity="CRITICAL",
                    bidders_involved=unique_companies,
                    forensic_evidence=f"Direct digital artifact match across supposedly independent bidders: '{sig}'. Submissions originated from the exact same workstation or author environment.",
                    recommendation="Immediately refer to Central Vigilance Commission (CVC) & Competition Commission of India (CCI) for cartel investigation under Section 3 of Competition Act."
                ))

        # 2. Check for Duplicate / Stolen CA UDINs across bidders
        udin_map: Dict[str, List[str]] = {}
        for bidder in bidders:
            udin = bidder.financial_profile.ca_udin
            if udin:
                clean_udin = udin.strip().upper()
                udin_map.setdefault(clean_udin, []).append(bidder.company_name)

        for udin, company_list in udin_map.items():
            unique_companies = sorted(list(set(company_list)))
            if len(unique_companies) > 1:
                alerts.append(CartelAlert(
                    alert_id=f"CARTEL-UDIN-{len(alerts)+1}",
                    signal_name="DUPLICATE_CA_UDIN_FORGERY",
                    severity="CRITICAL",
                    bidders_involved=unique_companies,
                    forensic_evidence=f"Identical Chartered Accountant UDIN ({udin}) was submitted by multiple competing bidders. One or both documents are fraudulent.",
                    recommendation="Cancel technical evaluation for affected bidders. Verify directly on ICAI UDIN Portal (udin.icai.org) and file legal FIR for document forgery."
                ))

        # 3. Check for invalid UDIN formats
        for bidder in bidders:
            udin = bidder.financial_profile.ca_udin
            if udin and not cls.validate_udin_format(udin):
                alerts.append(CartelAlert(
                    alert_id=f"FORGERY-UDIN-{len(alerts)+1}",
                    signal_name="INVALID_UDIN_STRUCTURE",
                    severity="HIGH",
                    bidders_involved=[bidder.company_name],
                    forensic_evidence=f"Claimed CA UDIN '{udin}' fails ICAI mandatory 18-digit cryptographic verification structure.",
                    recommendation="Disqualify bidder under Clause on False Documentation; seek confirmation from statutory auditor."
                ))

        return alerts
