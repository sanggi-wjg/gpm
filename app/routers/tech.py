import pickle
from typing import List

from fastapi import APIRouter, Depends, Path
from redis.client import Redis
from sqlalchemy.orm import Session
from starlette import status

from app.database.cache import get_redis
from app.database.database import get_db
from app.dependencies.query_depend import PageQueryParameter, TechStackSearch
from app.exceptions.exception import NotFound
from app.routers import RouterTags
from app.routers.auth import verify_admin_user
from app.schemas.tech_schema import TechCategory, TechCategoryRegister, TechStack, TechStackRegister
from app.schemas.user_schema import User
from app.service import tech_service

router = APIRouter(
    prefix="/api/v1",
    tags=[RouterTags.Tech],
    responses={404: {"detail": "not found"}}
)


@router.get("/tech-categories", response_model=List[TechCategory], status_code=status.HTTP_200_OK)
async def get_tech_categories(db: Session = Depends(get_db),
                              redis: Redis = Depends(get_redis)):
    redis_key = "tech-category:tech-stack:all"
    categories = redis.get(redis_key)

    if categories is None:
        response = tech_service.find_tech_category_all(db)
        _ = redis.setex(redis_key, 60 * 60, pickle.dumps(response))
        return response

    return pickle.loads(categories)


@router.post("/tech-categories", response_model=TechCategory, status_code=status.HTTP_201_CREATED)
async def create_tech_category(tech_category: TechCategoryRegister,
                               current_user: User = Depends(verify_admin_user),
                               db: Session = Depends(get_db)):
    return tech_service.create_tech_category(db, tech_category)


@router.get("/tech-categories/{tech_category_id}", response_model=TechCategory)
async def get_tech_category(tech_category_id: int = Path(gt=0),
                            db: Session = Depends(get_db)):
    find_tech_category = tech_service.find_tech_category_by_id(db, tech_category_id)
    if not find_tech_category:
        raise NotFound()
    return find_tech_category


@router.put("/tech-categories/{tech_category_id}", response_model=TechCategory, status_code=status.HTTP_200_OK)
async def change_tech_category(tech_category: TechCategoryRegister,
                               tech_category_id: int = Path(gt=0),
                               current_user: User = Depends(verify_admin_user),
                               db: Session = Depends(get_db)):
    return tech_service.update_tech_category(db, tech_category_id, tech_category)


@router.delete("/tech-categories/{tech_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tech_category(tech_category_id: int = Path(gt=0),
                               current_user: User = Depends(verify_admin_user),
                               db: Session = Depends(get_db)):
    tech_service.delete_tech_category(db, tech_category_id)


@router.get("/tech-stacks", response_model=List[TechStack], status_code=status.HTTP_200_OK)
async def get_tech_stacks_all(page_param: PageQueryParameter = Depends(),
                              db: Session = Depends(get_db)):
    return tech_service.find_tech_stack_all_by_paged(db, page_param.offset, page_param.limit)


@router.get("/tech-categories/{tech_category_id}/tech-stacks",
            response_model=List[TechStack],
            status_code=status.HTTP_200_OK)
async def get_tech_stacks(tech_category_id: int = Path(gt=0),
                          search: TechStackSearch = Depends(),
                          db: Session = Depends(get_db)):
    return tech_service.find_tech_stack_all_by_category_id_and_paged(
        db, tech_category_id, search.offset, search.limit, search
    )


@router.post("/tech-categories/{tech_category_id}/tech-stacks",
             response_model=TechStack,
             status_code=status.HTTP_201_CREATED)
async def create_tech_stack(tech_stack: TechStackRegister,
                            tech_category_id: int = Path(gt=0),
                            current_user: User = Depends(verify_admin_user),
                            db: Session = Depends(get_db)):
    return tech_service.create_tech_stack(db, tech_category_id, tech_stack)
