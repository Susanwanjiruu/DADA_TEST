from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user, require_support_provider
from app.schemas.organisations import OrganisationCreate, OrganisationRead
from app.services import organisations as org_service

router = APIRouter(prefix="/organisations", tags=["Organisations"])


@router.get("", response_model=list[OrganisationRead])
def get_organisations(
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    return org_service.list_organisations(db)


@router.post("", response_model=OrganisationRead, status_code=status.HTTP_201_CREATED)
def create_organisation(
    data: OrganisationCreate,
    db: Session = Depends(get_db),
    current_provider: Registration = Depends(require_support_provider),
):
    
    return org_service.create_organisation(db, data, owner=current_provider)