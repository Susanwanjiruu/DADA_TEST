import uuid
from sqlalchemy.orm import Session
from app.models.admin_actions import AdminAction


class AdminActionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, skip: int = 0, limit: int = 100) -> list[AdminAction]:
        return self.db.query(AdminAction).order_by(AdminAction.performed_at.desc()).offset(skip).limit(limit).all()

    def create(self, action: AdminAction) -> AdminAction:
        self.db.add(action)
        self.db.commit()
        self.db.refresh(action)
        return action