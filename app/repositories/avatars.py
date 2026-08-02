import uuid
from sqlalchemy.orm import Session
from app.models.avatars import Avatar


class AvatarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, avatar_id: uuid.UUID) -> Avatar | None:
        return self.db.query(Avatar).filter(Avatar.avatar_id == avatar_id).first()

    def list_all(self) -> list[Avatar]:
        return self.db.query(Avatar).all()

    def create(self, avatar: Avatar) -> Avatar:
        self.db.add(avatar)
        self.db.commit()
        self.db.refresh(avatar)
        return avatar

    def delete(self, avatar: Avatar) -> None:
        self.db.delete(avatar)
        self.db.commit()