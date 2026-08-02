import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user
from app.schemas.game_progress import GameProgressCreate, GameProgressUpdate, GameProgressRead
from app.services import game_progress as progress_service

router = APIRouter(prefix="/game-progress", tags=["Game Progress"])


@router.post("", response_model=GameProgressRead, status_code=status.HTTP_201_CREATED)
def start_game(
    data: GameProgressCreate,
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
   
    return progress_service.start_game(db, data, player=current_user)


@router.get("/me", response_model=list[GameProgressRead])
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    """Users see only their own play history."""
    return progress_service.list_my_progress(db, player=current_user)


@router.put("/{progress_id}", response_model=GameProgressRead)
def update_progress(
    progress_id: uuid.UUID,
    data: GameProgressUpdate,
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    
    return progress_service.update_progress(db, progress_id, data, requester=current_user)