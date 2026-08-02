from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user, require_admin
from app.schemas.registrations import (
    RegistrationCreate,
    RegistrationRead,
    RegistrationUpdate,
    AdminStatusUpdate,
    LoginRequest,
    TokenResponse,
)
from app.services import registrations as registration_service

router = APIRouter(tags=["Registrations & Authentication"])


@router.post("/auth/register", response_model=RegistrationRead, status_code=status.HTTP_201_CREATED)
def register_user(data: RegistrationCreate, db: Session = Depends(get_db)):
    """Open signup endpoint. Sets status to active and hashes password."""
    return registration_service.register_new_user(db, data)


@router.post("/auth/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    """Verifies credentials, checks account status, returns a signed JWT."""
    return registration_service.authenticate_user(db, data)


@router.get("/users/me", response_model=RegistrationRead)
def get_current_user_profile(current_user: Registration = Depends(get_current_user)):
    """Returns the profile of whoever the verified token belongs to."""
    return current_user


@router.put("/users/me", response_model=RegistrationRead)
def update_user_profile(
    data: RegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    """Lets a logged-in user update their own display name / avatar. Cannot touch other users."""
    return registration_service.update_profile(db, user_id=current_user.registration_id, data=data)


@router.get("/admin/registrations", response_model=list[RegistrationRead])
def admin_list_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    """Admin-only. Lists all platform accounts."""
    return registration_service.admin_list_users(db, skip=skip, limit=limit)


@router.patch("/admin/registrations/{registration_id}/status", response_model=RegistrationRead)
def admin_modify_user_status(
    registration_id: UUID,
    data: AdminStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    """Admin-only. Bans, suspends, or reactivates an account."""
    return registration_service.admin_toggle_status(db, target_user_id=registration_id, data=data)