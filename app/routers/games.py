import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.registrations import Registration
from app.core.security import get_current_user, require_admin
from app.schemas.games import GameCreate, GameUpdate, GameRead
from app.services import games as game_service

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("")
def get_games(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
) -> list[GameRead]:
    return game_service.list_games(db, skip=skip, limit=limit)


@router.get("/{game_id}", response_model=GameRead)
def get_game(
    game_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: Registration = Depends(get_current_user),
):
    return game_service.get_game(db, game_id)


@router.post("", response_model=GameRead, status_code=status.HTTP_201_CREATED)
def create_game(
    data: GameCreate,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    return game_service.create_game(db, data, creator=current_admin)


@router.put("/{game_id}", response_model=GameRead)
def update_game(
    game_id: uuid.UUID,
    data: GameUpdate,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    return game_service.update_game(db, game_id, data)


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
    game_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_admin: Registration = Depends(require_admin),
):
    game_service.delete_game(db, game_id)
