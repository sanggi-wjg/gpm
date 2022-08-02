import secrets
from typing import List

from sqlalchemy.orm import Session

from app.database.models import UserEntity, UserProvider
from app.exceptions.exception import DuplicateError
from app.schemas import user_schema


def find_user_all_by_paged(db: Session, offset: int, limit: int) -> List[UserEntity]:
    return db.query(UserEntity).offset(offset).limit(limit).all()


def find_user_by_email(db: Session, email: str) -> UserEntity:
    return db.query(UserEntity).filter(
        UserEntity.email == email
    ).first()


def find_user_by_email_and_provider(db: Session, email: str, provider: UserProvider) -> UserEntity:
    return db.query(UserEntity).filter(
        UserEntity.email == email,
        UserEntity.provider == provider
    ).first()


def create_user(db: Session, user_register: user_schema.UserRegister) -> UserEntity:
    find_user = find_user_by_email(db, user_register.email)
    if find_user:
        raise DuplicateError(user_register.email)

    new_user = UserEntity(
        email=user_register.email,
        hashed_password=user_register.hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_provider_user(db: Session, user_register: user_schema.UserProvidedRegister) -> UserEntity:
    find_user = find_user_by_email(db, user_register.email)
    if find_user:
        raise DuplicateError(user_register.email)

    new_user = UserEntity(
        email=user_register.email,
        hashed_password=secrets.token_hex(16),
        provider=user_register.provider,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_admin_user(db: Session, user_register: user_schema.UserRegister) -> UserEntity:
    find_user = find_user_by_email(db, user_register.email)
    if find_user:
        raise DuplicateError(user_register.email)

    new_user = UserEntity(
        email=user_register.email,
        hashed_password=user_register.hashed_password,
        is_admin=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
