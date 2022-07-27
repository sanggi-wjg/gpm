from typing import List

from sqlalchemy.orm import Session

from app.database.models import UserEntity
from app.schemas import user_schema


def find_user_all(db: Session) -> List[UserEntity]:
    return db.query(UserEntity).all()


def find_user_all_by_paged(db: Session, offset: int, limit: int) -> List[UserEntity]:
    return db.query(UserEntity).offset(offset).limit(limit).all()


def find_user_by_email(db: Session, email: str) -> UserEntity:
    return db.query(UserEntity).filter(UserEntity.email == email).first()


def create_user(db: Session, user: user_schema.UserRegister) -> UserEntity:
    new_user = UserEntity(
        email=user.email,
        hashed_password=user.hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
