import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user, require_admin
from app.schemas.avatars import AvatarCreate, AvatarRead
from app.services import avatars as avatar_service

router = APIRouter(prefix="/avatars", tags=["Avatars"])


@router.get("", response_model=list[AvatarRead])
def get_avatars(db: Session = Depends(get_db), current_user: Registration = Depends(get_current_user)):
    """Any logged-in user can browse avatar choices. No sensitive data here."""
    return avatar_service.list_avatars(db)


@router.post("", response_model=AvatarRead, status_code=status.HTTP_201_CREATED)
def create_avatar(
    data: AvatarCreate,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    """Admin-only: add a new avatar option."""
    return avatar_service.create_avatar(db, data)


@router.delete("/{avatar_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(
    avatar_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    """Admin-only: remove an avatar option."""
    avatar_service.delete_avatar(db, avatar_id)