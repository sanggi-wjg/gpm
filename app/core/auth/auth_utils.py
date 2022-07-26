from passlib.context import CryptContext

crypt = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return crypt.hash(plain_password)
