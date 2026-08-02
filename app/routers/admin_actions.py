from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import require_admin
from app.schemas.admin_actions import AdminActionRead
from app.services import admin_actions as action_service

router = APIRouter(prefix="/admin/actions", tags=["Admin Audit Log"])


@router.get("", response_model=list[AdminActionRead])
def get_admin_actions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    
    return action_service.list_actions(db, skip=skip, limit=limit)