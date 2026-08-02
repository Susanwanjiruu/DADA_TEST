import uuid
import enum
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class RequestStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"


class SupportRequest(Base):
    __tablename__ = "support_requests"

    support_request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.registration_id"), nullable=False)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey("organisations.organisation_id"), nullable=False)
    problem_description = Column(String, nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    request_status = Column(Enum(RequestStatus), nullable=False, default=RequestStatus.pending)

    user = relationship("Registration", back_populates="support_requests")
    organisation = relationship("Organisation", back_populates="support_requests")