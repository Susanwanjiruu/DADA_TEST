import uuid
from pydantic import BaseModel


class AvatarCreate(BaseModel):
    avatar_url: str
    avatar_name: str


class AvatarRead(BaseModel):
    avatar_id: uuid.UUID
    avatar_url: str
    avatar_name: str

    model_config = {"from_attributes": True}