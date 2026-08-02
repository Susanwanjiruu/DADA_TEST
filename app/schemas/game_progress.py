import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.game_progress import CompletionStatus


class GameProgressCreate(BaseModel):
    game_id: uuid.UUID


class GameProgressUpdate(BaseModel):
    score: Optional[int] = None
    completion_status: CompletionStatus


class GameProgressRead(BaseModel):
    progress_id: uuid.UUID
    game_id: uuid.UUID
    registration_id: uuid.UUID
    score: Optional[int] = None
    completion_status: CompletionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}