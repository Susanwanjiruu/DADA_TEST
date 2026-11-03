import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.game_progress import CompletionStatus


class GameProgressCreate(BaseModel):
    game_id: uuid.UUID


class GameProgressUpdate(BaseModel):
    # The project has no shared maximum-score definition, so enforce the
    # universal constraint (non-negative) without inventing a game-specific cap.
    score: Optional[int] = Field(default=None, ge=0)
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
