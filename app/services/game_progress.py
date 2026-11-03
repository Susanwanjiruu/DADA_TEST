import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.game_progress import GameProgress, CompletionStatus
from app.models.registrations import Registration, UserType
from app.repositories.game_progress import GameProgressRepository
from app.schemas.game_progress import GameProgressCreate, GameProgressUpdate


def start_game(db: Session, data: GameProgressCreate, player: Registration) -> GameProgress:
    repo = GameProgressRepository(db)
    progress = GameProgress(
        progress_id=uuid.uuid4(),
        game_id=data.game_id,
        registration_id=player.registration_id,
        completion_status=CompletionStatus.in_progress,
        started_at=datetime.now(timezone.utc),
    )
    return repo.create(progress)


def list_my_progress(db: Session, player: Registration) -> list[GameProgress]:
    return GameProgressRepository(db).list_for_user(player.registration_id)


def update_progress(
    db: Session,
    progress_id: uuid.UUID,
    data: GameProgressUpdate,
    requester: Registration,
) -> GameProgress:
    repo = GameProgressRepository(db)
    progress = repo.get_by_id(progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")

    is_admin = requester.user_type == UserType.admin

    # Players may only update their own play sessions.
    if progress.registration_id != requester.registration_id and not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to modify this progress record",
        )

    # A player's completed or abandoned session is final. Administrators can
    # correct records when necessary.
    if (
        not is_admin
        and progress.completion_status != CompletionStatus.in_progress
    ):
        raise HTTPException(
            status_code=409,
            detail="This game session is already final and cannot be changed",
        )

    progress.score = data.score
    progress.completion_status = data.completion_status

    if data.completion_status in (
        CompletionStatus.completed,
        CompletionStatus.abandoned,
    ):
        progress.completed_at = datetime.now(timezone.utc)
    else:
        # Keep the timestamp consistent if an administrator reopens a session.
        progress.completed_at = None

    return repo.update(progress)
