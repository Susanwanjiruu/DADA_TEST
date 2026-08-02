import uuid
from pydantic import BaseModel


class OrganisationCreate(BaseModel):
    organisation_name: str


class OrganisationRead(BaseModel):
    organisation_id: uuid.UUID
    registration_id: uuid.UUID
    organisation_name: str

    model_config = {"from_attributes": True}