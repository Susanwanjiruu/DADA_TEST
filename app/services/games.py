import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.games import Game
from app.models.registrations import Registration
from app.repositories.games import GameRepository
from app.schemas.games import GameCreate, GameUpdate


def list_games(db: Session, skip: int = 0, limit: int = 100) -> list[Game]:
    return GameRepository(db).list_all(skip=skip, limit=limit)


def get_game(db: Session, game_id: uuid.UUID) -> Game:
    game = GameRepository(db).get_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def create_game(db: Session, data: GameCreate, creator: Registration) -> Game:
    repo = GameRepository(db)
    game = Game(
        game_id=uuid.uuid4(),
        registration_id=creator.registration_id,
        game_title=data.game_title,
        game_type=data.game_type,
        games_sub_type=data.games_sub_type,
        game_payload=data.game_payload,
        file_uri=data.file_uri,
    )
    return repo.create(game)


def update_game(db: Session, game_id: uuid.UUID, data: GameUpdate) -> Game:
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if data.game_title is not None:
        game.game_title = data.game_title
    if data.game_payload is not None:
        game.game_payload = data.game_payload

    return repo.update(game)


def delete_game(db: Session, game_id: uuid.UUID) -> None:
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    repo.delete(game)