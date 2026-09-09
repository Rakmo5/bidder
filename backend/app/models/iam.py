from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class UserRole(str, Enum):
    OCR_OPERATOR = "OCR_OPERATOR"                     # Ingestion, OCR trigger, scan verification
    TECHNICAL_SCRUTINIZER = "TECHNICAL_SCRUTINIZER"   # Review compliance, verify evidence, submit remarks
    CHIEF_EXECUTIVE = "CHIEF_EXECUTIVE"               # Committee Chairman: Threshold tuning, final QCBS approval
    VIGILANCE_OFFICER = "VIGILANCE_OFFICER"           # CVC: Cartel audit, forensics, tamper-proof logs

class UserPermission(str, Enum):
    UPLOAD_DOCUMENTS = "UPLOAD_DOCUMENTS"
    TRIGGER_OCR = "TRIGGER_OCR"
    VERIFY_COMPLIANCE = "VERIFY_COMPLIANCE"
    MODIFY_THRESHOLDS = "MODIFY_THRESHOLDS"
    APPROVE_EVALUATION = "APPROVE_EVALUATION"
    VIEW_FORENSICS = "VIEW_FORENSICS"
    EXPORT_REPORTS = "EXPORT_REPORTS"
    VIEW_AUDIT_LOGS = "VIEW_AUDIT_LOGS"

class UserProfile(BaseModel):
    id: str
    name: str
    designation: str
    department: str
    role: UserRole
    permissions: List[UserPermission] = []
    avatar_url: Optional[str] = None

class AuditLogEntry(BaseModel):
    log_id: str
    timestamp: str
    user_id: str
    user_name: str
    role: UserRole
    action: str  # e.g., "THRESHOLD_MODIFIED", "OCR_TRIGGERED", "CARTEL_FLAGGED", "QCBS_APPROVED"
    target_entity: str  # e.g., "Tender: MOPNG-TND-2024-881"
    details: str
    ip_address: str = "127.0.0.1"
