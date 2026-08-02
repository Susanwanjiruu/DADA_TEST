import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.organisations import Organisation
from app.models.registrations import Registration
from app.repositories.organisations import OrganisationRepository
from app.schemas.organisations import OrganisationCreate


def list_organisations(db: Session) -> list[Organisation]:
    return OrganisationRepository(db).list_all()


def create_organisation(db: Session, data: OrganisationCreate, owner: Registration) -> Organisation:
    repo = OrganisationRepository(db)

    if repo.get_by_registration_id(owner.registration_id):
        raise HTTPException(status_code=400, detail="This account already has an organisation profile")

    org = Organisation(
        organisation_id=uuid.uuid4(),
        registration_id=owner.registration_id,
        organisation_name=data.organisation_name,
    )
    return repo.create(org)