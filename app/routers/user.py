from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.query_depend import PageQueryParameter, page_parameter
from app.exceptions.user_exception import DuplicateEmail
from app.database.database import get_db

from app.routers import RouterTags
from app.repositories import user_repo
from app.routers.auth import verify_current_user
from app.schemas.user_schema import User, RegisterUser

router = APIRouter(
    prefix="/api/v1",
    tags=[RouterTags.User],
    responses={404: {"detail": "not found"}}
)


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(page_param: PageQueryParameter = Depends(page_parameter),
                    current_user: User = Depends(verify_current_user),
                    db: Session = Depends(get_db)):
    return user_repo.find_users_by_paged(db, page_param.offset, page_param.limit)


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: RegisterUser,
                          current_user: User = Depends(verify_current_user),
                          db: Session = Depends(get_db)):
    find_user = user_repo.find_user_by_email(db, user.email)
    if find_user:
        raise DuplicateEmail(user.email)

    new_user = user_repo.create_user(db, user)
    return new_user
