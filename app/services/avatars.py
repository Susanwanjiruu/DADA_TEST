import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.avatars import Avatar
from app.repositories.avatars import AvatarRepository
from app.schemas.avatars import AvatarCreate


def list_avatars(db: Session) -> list[Avatar]:
    return AvatarRepository(db).list_all()


def create_avatar(db: Session, data: AvatarCreate) -> Avatar:
    repo = AvatarRepository(db)
    avatar = Avatar(avatar_id=uuid.uuid4(), avatar_url=data.avatar_url, avatar_name=data.avatar_name)
    return repo.create(avatar)


def delete_avatar(db: Session, avatar_id: uuid.UUID) -> None:
    repo = AvatarRepository(db)
    avatar = repo.get_by_id(avatar_id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    repo.delete(avatar)