import uuid
from sqlalchemy.orm import Session
from app.models.game_progress import GameProgress


class GameProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, progress_id: uuid.UUID) -> GameProgress | None:
        return self.db.query(GameProgress).filter(GameProgress.progress_id == progress_id).first()

    def list_for_user(self, registration_id: uuid.UUID) -> list[GameProgress]:
        return self.db.query(GameProgress).filter(GameProgress.registration_id == registration_id).all()

    def create(self, progress: GameProgress) -> GameProgress:
        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def update(self, progress: GameProgress) -> GameProgress:
        self.db.commit()
        self.db.refresh(progress)
        return progress