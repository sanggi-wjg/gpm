from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions.user_exception import DuplicateEmail
from app.database.database import get_db

from app.routers import RouterTags
from app.repositories import user_repo
from app.schemas.user_schema import User, RegisterUser

router = APIRouter(
    prefix="/api/v1/users",
    tags=[RouterTags.User],
    responses={404: {"detail": "not found"}}
)


@router.get("", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    return user_repo.find_users(db)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: RegisterUser, db: Session = Depends(get_db)):
    if user_repo.is_exist_user_by_email(db, user.email):
        raise DuplicateEmail(user.email)

    new_user = user_repo.create_user(db, user)
    return new_user
