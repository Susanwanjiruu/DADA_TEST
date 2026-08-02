import uuid
import enum
from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class CompletionStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class GameProgress(Base):
    __tablename__ = "game_progress"

    progress_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.game_id"), nullable=False)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.registration_id"), nullable=False)
    score = Column(Integer, nullable=True)
    completion_status = Column(Enum(CompletionStatus), nullable=False, default=CompletionStatus.in_progress)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    game = relationship("Game", back_populates="game_progress")
    player = relationship("Registration", back_populates="game_progress")