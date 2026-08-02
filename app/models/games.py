import uuid
import enum
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database import Base


class GameType(str, enum.Enum):
    quiz = "quiz"
    puzzle = "puzzle"
    scenario = "scenario"


class GameSubType(str, enum.Enum):
    word_scramble = "word_scramble"
    crossword = "crossword"
    word_search = "word_search"


class Game(Base):
    __tablename__ = "games"

    game_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.registration_id"), nullable=False)
    game_title = Column(String, nullable=False)
    game_type = Column(Enum(GameType), nullable=False)
    games_sub_type = Column(Enum(GameSubType), nullable=True)
    game_payload = Column(JSONB, nullable=False)
    file_uri = Column(String, nullable=False)
    game_created_at = Column(DateTime(timezone=True), server_default=func.now())
    game_updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    creator = relationship("Registration", back_populates="games")
    game_progress = relationship("GameProgress", back_populates="game")