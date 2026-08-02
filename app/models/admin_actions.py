import uuid
import enum
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class ActionType(str, enum.Enum):
    ban_user = "ban_user"
    suspend_user = "suspend_user"
    enable_feature = "enable_feature"
    disable_feature = "disable_feature"


class AdminAction(Base):
    __tablename__ = "admin_actions"

    action_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.registration_id"), nullable=False)
    action_type = Column(Enum(ActionType), nullable=False)
    action_details = Column(String, nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())

    admin = relationship("Registration", back_populates="admin_actions")