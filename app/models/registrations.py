import uuid
import enum
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class UserType(str, enum.Enum):
    admin = "admin"
    support_provider = "support_provider"
    player = "player"


class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    prefer_not_to_say = "prefer_not_to_say"


class AccountStatus(str, enum.Enum):
    active = "active"
    banned = "banned"
    suspended = "suspended"


class Registration(Base):
    __tablename__ = "registrations"

    registration_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.avatar_id"), nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    encrypted_phone_number = Column(String, nullable=True)
    account_status = Column(Enum(AccountStatus), nullable=False, default=AccountStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    avatar = relationship("Avatar", back_populates="registrations")
    games = relationship("Game", back_populates="creator")
    game_progress = relationship("GameProgress", back_populates="player")
    organisation = relationship("Organisation", back_populates="registration", uselist=False)
    support_requests = relationship("SupportRequest", back_populates="user")
    admin_actions = relationship("AdminAction", back_populates="admin")