import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.support_requests import SupportRequest
from app.models.registrations import Registration
from app.models.organisations import Organisation
from app.repositories.support_requests import SupportRequestRepository
from app.repositories.organisations import OrganisationRepository
from app.schemas.support_requests import SupportRequestCreate, SupportRequestStatusUpdate


def create_support_request(db: Session, data: SupportRequestCreate, requester: Registration) -> SupportRequest:
    org_repo = OrganisationRepository(db)
    if not org_repo.get_by_id(data.organisation_id):
        raise HTTPException(status_code=404, detail="Organisation not found")

    repo = SupportRequestRepository(db)
    request = SupportRequest(
        support_request_id=uuid.uuid4(),
        registration_id=requester.registration_id,
        organisation_id=data.organisation_id,
        problem_description=data.problem_description,
    )
    return repo.create(request)


def list_my_requests(db: Session, requester: Registration) -> list[SupportRequest]:
    return SupportRequestRepository(db).list_for_user(requester.registration_id)


def list_requests_for_my_org(db: Session, provider: Registration) -> list[SupportRequest]:
    """Support providers only see requests routed to their own organisation, never all requests platform-wide."""
    org = OrganisationRepository(db).get_by_registration_id(provider.registration_id)
    if not org:
        raise HTTPException(status_code=404, detail="No organisation profile linked to this account")
    return SupportRequestRepository(db).list_for_organisation(org.organisation_id)


def update_request_status(
    db: Session, support_request_id: uuid.UUID, data: SupportRequestStatusUpdate, provider: Registration
) -> SupportRequest:
    repo = SupportRequestRepository(db)
    request = repo.get_by_id(support_request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Support request not found")

    org = OrganisationRepository(db).get_by_registration_id(provider.registration_id)
    if not org or request.organisation_id != org.organisation_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this request")

    request.request_status = data.request_status
    return repo.update(request)