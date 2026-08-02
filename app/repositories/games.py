import uuid
from sqlalchemy.orm import Session
from app.models.games import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, game_id: uuid.UUID) -> Game | None:
        return self.db.query(Game).filter(Game.game_id == game_id).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Game]:
        return self.db.query(Game).offset(skip).limit(limit).all()

    def create(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def update(self, game: Game) -> Game:
        self.db.commit()
        self.db.refresh(game)
        return game

    def delete(self, game: Game) -> None:
        self.db.delete(game)
        self.db.commit()