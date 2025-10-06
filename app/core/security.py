from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72  # bcrypt limit


def _truncate_password(password: str) -> bytes:
    """
    Encode password to UTF-8 and truncate to 72 bytes for bcrypt
    """
    return password.encode("utf-8")[:MAX_BCRYPT_BYTES]


def get_password_hash(password: str) -> str:
    truncated = _truncate_password(password)
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = _truncate_password(plain_password)
    return pwd_context.verify(truncated, hashed_password)


def create_access_token(data: dict, expires_delta: int = 3600):
    """
    Create JWT token with optional expiry (default 1 hour)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
