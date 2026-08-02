import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.support_requests import RequestStatus


class SupportRequestCreate(BaseModel):
    organisation_id: uuid.UUID
    problem_description: str


class SupportRequestStatusUpdate(BaseModel):
    request_status: RequestStatus


class SupportRequestRead(BaseModel):
    support_request_id: uuid.UUID
    registration_id: uuid.UUID
    organisation_id: uuid.UUID
    problem_description: str
    requested_at: datetime
    request_status: RequestStatus

    model_config = {"from_attributes": True}