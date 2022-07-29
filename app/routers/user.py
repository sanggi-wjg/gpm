from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.query_depend import PageQueryParameter, page_parameter
from app.database.database import get_db

from app.routers import RouterTags
from app.service import user_service
from app.routers.auth import verify_current_user
from app.schemas.user_schema import User, UserRegister

router = APIRouter(
    prefix="/api/v1",
    tags=[RouterTags.User],
    responses={404: {"detail": "not found"}}
)


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(page_param: PageQueryParameter = Depends(page_parameter),
                    current_user: User = Depends(verify_current_user),
                    db: Session = Depends(get_db)):
    return user_service.find_user_all_by_paged(db, page_param.offset, page_param.limit)


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRegister,
                      current_user: User = Depends(verify_current_user),
                      db: Session = Depends(get_db)):
    return user_service.create_user(db, user)
