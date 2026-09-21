import datetime
import uuid
from typing import List, Optional
from app.models.iam import UserProfile, UserRole, UserPermission, AuditLogEntry

# Pre-configured Highway Evaluation Personas
DEFAULT_USERS = [
    UserProfile(
        id="USR-EXEC-01",
        name="Shri Rajesh Kumar, IAS",
        designation="Additional Secretary & Member (Technical)",
        department="National Highways Authority of India (NHAI) / MoRTH",
        role=UserRole.CHIEF_EXECUTIVE,
        permissions=[
            UserPermission.MODIFY_THRESHOLDS,
            UserPermission.APPROVE_EVALUATION,
            UserPermission.EXPORT_REPORTS,
            UserPermission.VIEW_FORENSICS,
            UserPermission.VIEW_AUDIT_LOGS
        ]
    ),
    UserProfile(
        id="USR-TECH-02",
        name="Dr. Priya Sharma",
        designation="Chief Engineer (Highways & Quality Control)",
        department="Ministry of Road Transport and Highways (MoRTH)",
        role=UserRole.TECHNICAL_SCRUTINIZER,
        permissions=[
            UserPermission.VERIFY_COMPLIANCE,
            UserPermission.UPLOAD_DOCUMENTS,
            UserPermission.EXPORT_REPORTS
        ]
    ),
    UserProfile(
        id="USR-VIG-03",
        name="Shri Anil Verma",
        designation="Chief Vigilance Officer (CVO)",
        department="Central Vigilance Commission (CVC) / NHAI Vigilance",
        role=UserRole.VIGILANCE_OFFICER,
        permissions=[
            UserPermission.VIEW_FORENSICS,
            UserPermission.VIEW_AUDIT_LOGS,
            UserPermission.EXPORT_REPORTS
        ]
    ),
    UserProfile(
        id="USR-OCR-04",
        name="Suresh Patil",
        designation="Material Testing & Document Ingestion Officer",
        department="Central Road Research Institute (CRRI) / NIC Procurement Support",
        role=UserRole.OCR_OPERATOR,
        permissions=[
            UserPermission.UPLOAD_DOCUMENTS,
            UserPermission.TRIGGER_OCR
        ]
    )
]

AUDIT_LOGS: List[AuditLogEntry] = []

class IAMService:
    @staticmethod
    def get_all_users() -> List[UserProfile]:
        return DEFAULT_USERS

    @staticmethod
    def get_user_by_role(role: UserRole) -> Optional[UserProfile]:
        return next((u for u in DEFAULT_USERS if u.role == role), None)

    @staticmethod
    def log_action(user: UserProfile, action: str, target: str, details: str):
        entry = AuditLogEntry(
            log_id=f"LOG-{uuid.uuid4().hex[:6].upper()}",
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id=user.id,
            user_name=user.name,
            role=user.role,
            action=action,
            target_entity=target,
            details=details
        )
        AUDIT_LOGS.insert(0, entry) # Most recent first
        return entry

    @staticmethod
    def get_audit_logs() -> List[AuditLogEntry]:
        return AUDIT_LOGS

# Seed initial logs
_admin = DEFAULT_USERS[0]
IAMService.log_action(_admin, "SYSTEM_INITIALIZATION", "MoRTH Highway Scrutiny Engine", "System initialized with IRC:37-2018 & CVC Anti-Cartel Mode Active")
IAMService.log_action(DEFAULT_USERS[3], "SAMPLE_DATA_LOADED", "Tender: MORTH-NH-2024-402", "Ingested NHAI 4-Lane Greenfield Bypass EPC Tender & 3 Contractor Dossiers")

