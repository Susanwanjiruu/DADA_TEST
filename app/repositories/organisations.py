import uuid
from sqlalchemy.orm import Session
from app.models.organisations import Organisation


class OrganisationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, organisation_id: uuid.UUID) -> Organisation | None:
        return self.db.query(Organisation).filter(Organisation.organisation_id == organisation_id).first()

    def get_by_registration_id(self, registration_id: uuid.UUID) -> Organisation | None:
        return self.db.query(Organisation).filter(Organisation.registration_id == registration_id).first()

    def list_all(self) -> list[Organisation]:
        return self.db.query(Organisation).all()

    def create(self, organisation: Organisation) -> Organisation:
        self.db.add(organisation)
        self.db.commit()
        self.db.refresh(organisation)
        return organisation