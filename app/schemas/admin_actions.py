import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.admin_actions import ActionType


class AdminActionRead(BaseModel):
    action_id: uuid.UUID
    registration_id: uuid.UUID
    action_type: ActionType
    action_details: str
    performed_at: datetime

    model_config = {"from_attributes": True}