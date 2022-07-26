from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.database.models import UserEntity
from app.schemas import user_schema


def find_users(db: Session) -> List[UserEntity]:
    return db.query(UserEntity).all()


def find_user_by_email(db: Session, email: str) -> UserEntity:
    return db.query(UserEntity).filter(UserEntity.email == email).first()


def is_exist_user_by_email(db: Session, email: str) -> bool:
    try:
        db.query(UserEntity).filter(UserEntity.email == email).one()
        return True
    except NoResultFound:
        return False


def create_user(db: Session, user: user_schema.RegisterUser) -> UserEntity:
    new_user = UserEntity(
        email = user.email,
        hashed_password = user.hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
