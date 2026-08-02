import uuid
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel
from app.models.games import GameType, GameSubType


class GameCreate(BaseModel):
    game_title: str
    game_type: GameType
    games_sub_type: Optional[GameSubType] = None
    game_payload: dict[str, Any]
    file_uri: str


class GameUpdate(BaseModel):
    game_title: Optional[str] = None
    game_payload: Optional[dict[str, Any]] = None


class GameRead(BaseModel):
    game_id: uuid.UUID
    registration_id: uuid.UUID
    game_title: str
    game_type: GameType
    games_sub_type: Optional[GameSubType] = None
    game_payload: dict[str, Any]
    file_uri: str
    game_created_at: datetime
    game_updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}