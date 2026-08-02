import uuid
from sqlalchemy.orm import Session
from app.models.registrations import Registration


class RegistrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, registration_id: uuid.UUID) -> Registration | None:
        return self.db.query(Registration).filter(
            Registration.registration_id == registration_id
        ).first()

    def get_by_email(self, email: str) -> Registration | None:
        return self.db.query(Registration).filter(
            Registration.email == email
        ).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Registration]:
        return self.db.query(Registration).offset(skip).limit(limit).all()

    def create(self, registration: Registration) -> Registration:
        self.db.add(registration)
        self.db.commit()
        self.db.refresh(registration)
        return registration

    def update(self, registration: Registration) -> Registration:
        self.db.commit()
        self.db.refresh(registration)
        return registration