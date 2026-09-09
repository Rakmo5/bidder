from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models.iam import UserProfile, AuditLogEntry, UserRole
from app.services.iam_service import IAMService

router = APIRouter()

@router.get("/users", response_model=List[UserProfile])
async def get_all_users():
    return IAMService.get_all_users()

@router.get("/audit-logs", response_model=List[AuditLogEntry])
async def get_audit_logs():
    return IAMService.get_audit_logs()

@router.post("/log")
async def create_audit_log(
    role: UserRole = Query(...),
    action: str = Query(...),
    target: str = Query(...),
    details: str = Query(...)
):
    user = IAMService.get_user_by_role(role)
    if not user:
        raise HTTPException(status_code=404, detail="Role persona not found")
    entry = IAMService.log_action(user, action, target, details)
    return {"status": "SUCCESS", "log_entry": entry}
