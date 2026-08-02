import uuid
from sqlalchemy.orm import Session

from app.models.admin_actions import AdminAction, ActionType
from app.repositories.admin_actions import AdminActionRepository


def log_action(db: Session, admin_id: uuid.UUID, action_type: ActionType, details: str) -> AdminAction:
  
    repo = AdminActionRepository(db)
    action = AdminAction(
        action_id=uuid.uuid4(),
        registration_id=admin_id,
        action_type=action_type,
        action_details=details,
    )
    return repo.create(action)


def list_actions(db: Session, skip: int = 0, limit: int = 100) -> list[AdminAction]:
    return AdminActionRepository(db).list_all(skip=skip, limit=limit)