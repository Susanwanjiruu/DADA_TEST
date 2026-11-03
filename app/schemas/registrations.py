import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models.registrations import UserType, Gender, AccountStatus


class RegistrationCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: Gender
    phone_number: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 10:
            raise ValueError("Password must be at least 10 characters")
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError("Password must include an uppercase letter and a number")
        return v


class RegistrationRead(BaseModel):
    registration_id: uuid.UUID
    avatar_id: Optional[uuid.UUID] = None
    email: EmailStr
    user_type: UserType
    name: str
    gender: Gender
    account_status: AccountStatus

    model_config = {"from_attributes": True}


class RegistrationUpdate(BaseModel):
    name: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None


class AdminStatusUpdate(BaseModel):
    account_status: AccountStatus


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
