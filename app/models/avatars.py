import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class Avatar(Base):
    __tablename__ = "avatars"

    avatar_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    avatar_url = Column(String, nullable=False)
    avatar_name = Column(String, nullable=False)

    registrations = relationship("Registration", back_populates="avatar")