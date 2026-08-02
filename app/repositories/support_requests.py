import uuid
from sqlalchemy.orm import Session
from app.models.support_requests import SupportRequest


class SupportRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, support_request_id: uuid.UUID) -> SupportRequest | None:
        return self.db.query(SupportRequest).filter(
            SupportRequest.support_request_id == support_request_id
        ).first()

    def list_for_user(self, registration_id: uuid.UUID) -> list[SupportRequest]:
        return self.db.query(SupportRequest).filter(
            SupportRequest.registration_id == registration_id
        ).all()

    def list_for_organisation(self, organisation_id: uuid.UUID) -> list[SupportRequest]:
        return self.db.query(SupportRequest).filter(
            SupportRequest.organisation_id == organisation_id
        ).all()

    def create(self, support_request: SupportRequest) -> SupportRequest:
        self.db.add(support_request)
        self.db.commit()
        self.db.refresh(support_request)
        return support_request

    def update(self, support_request: SupportRequest) -> SupportRequest:
        self.db.commit()
        self.db.refresh(support_request)
        return support_request