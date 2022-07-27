from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_config_settings

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_config_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return crypt.hash(plain_password)


def create_jwt_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.access_token_algorithm)
