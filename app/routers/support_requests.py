import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user, require_support_provider
from app.schemas.support_requests import SupportRequestCreate, SupportRequestStatusUpdate, SupportRequestRead
from app.services import support_requests as support_service

router = APIRouter(prefix="/support-requests", tags=["Support Requests"])


@router.post("", response_model=SupportRequestRead, status_code=status.HTTP_201_CREATED)
def create_support_request(
    data: SupportRequestCreate,
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
   
    return support_service.create_support_request(db, data, requester=current_user)


@router.get("/me", response_model=list[SupportRequestRead])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    
    return support_service.list_my_requests(db, requester=current_user)


@router.get("/inbox", response_model=list[SupportRequestRead])
def get_org_inbox(
    db: Session = Depends(get_db),
    current_provider: Registration = Depends(require_support_provider),
):
   
    return support_service.list_requests_for_my_org(db, provider=current_provider)


@router.patch("/{support_request_id}/status", response_model=SupportRequestRead)
def update_status(
    support_request_id: uuid.UUID,
    data: SupportRequestStatusUpdate,
    db: Session = Depends(get_db),
    current_provider: Registration = Depends(require_support_provider),
):
   
    return support_service.update_request_status(db, support_request_id, data, provider=current_provider)