from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from app.core.config import get_settings
from database import get_db
from app.models.registrations import Registration, UserType

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(settings.phone_encryption_key.encode())
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def encrypt_phone(phone: str) -> str:
    return fernet.encrypt(phone.encode()).decode()


def decrypt_phone(encrypted_phone: str) -> str:
    return fernet.decrypt(encrypted_phone.encode()).decode()


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("Missing subject claim")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Registration:
    registration_id = decode_access_token(token)
    try:
        parsed_id = uuid.UUID(registration_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token subject")

    user = db.query(Registration).filter(Registration.registration_id == parsed_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if user.account_status != "active":
        raise HTTPException(status_code=403, detail="Account is not active")
    return user


def require_admin(current_user: Registration = Depends(get_current_user)) -> Registration:
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


def require_support_provider(current_user: Registration = Depends(get_current_user)) -> Registration:
    if current_user.user_type != UserType.support_provider:
        raise HTTPException(status_code=403, detail="Support provider privileges required")
    return current_user