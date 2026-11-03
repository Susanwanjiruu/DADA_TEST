import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.registrations import Registration, AccountStatus, UserType
from app.repositories.registrations import RegistrationRepository
from app.schemas.registrations import (
    RegistrationCreate,
    RegistrationUpdate,
    AdminStatusUpdate,
    LoginRequest,
    TokenResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    encrypt_phone,
    create_access_token,
)


def register_new_user(db: Session, data: RegistrationCreate) -> Registration:
    repo = RegistrationRepository(db)

    if repo.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Registration(
        registration_id=uuid.uuid4(),
        email=data.email,
        hashed_password=hash_password(data.password),
        user_type=UserType.player,
        name=data.name,
        gender=data.gender,
        encrypted_phone_number=encrypt_phone(data.phone_number) if data.phone_number else None,
        account_status=AccountStatus.active,
    )
    return repo.create(new_user)


def authenticate_user(db: Session, data: LoginRequest) -> TokenResponse:
    repo = RegistrationRepository(db)
    user = repo.get_by_email(data.email)

    # Same error for "no such user" and "wrong password" — don't leak which one it was
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if user.account_status != AccountStatus.active:
        raise HTTPException(status_code=403, detail="Account is not active")

    token = create_access_token(subject=str(user.registration_id))
    return TokenResponse(access_token=token)


def get_profile(db: Session, user_id: uuid.UUID) -> Registration:
    repo = RegistrationRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_profile(db: Session, user_id: uuid.UUID, data: RegistrationUpdate) -> Registration:
    repo = RegistrationRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name
    if data.avatar_id is not None:
        user.avatar_id = data.avatar_id

    return repo.update(user)


def admin_list_users(db: Session, skip: int = 0, limit: int = 100) -> list[Registration]:
    repo = RegistrationRepository(db)
    return repo.list_all(skip=skip, limit=limit)


def admin_toggle_status(db: Session, target_user_id: uuid.UUID, data: AdminStatusUpdate) -> Registration:
    repo = RegistrationRepository(db)
    user = repo.get_by_id(target_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.account_status = data.account_status
    return repo.update(user)
