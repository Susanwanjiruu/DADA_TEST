import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    organisation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.registration_id"), nullable=False, unique=True)
    organisation_name = Column(String, nullable=False)

    registration = relationship("Registration", back_populates="organisation")
    support_requests = relationship("SupportRequest", back_populates="organisation")