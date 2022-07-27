from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.dependencies.query_depend import page_parameter, PageQueryParameter
from app.exceptions.exception import NotFound
from app.exceptions.tech_category_exception import DuplicateTechCategoryName
from app.service import tech_category_service
from app.routers import RouterTags
from app.schemas.tech_category_schema import TechCategory, RegisterTechCategory

router = APIRouter(
    prefix="/api/v1",
    tags=[RouterTags.TechCategory],
    responses={404: {"detail": "not found"}}
)


@router.get("/tech-categories", response_model=List[TechCategory], status_code=status.HTTP_200_OK)
async def get_tech_categories(page_param: PageQueryParameter = Depends(page_parameter), db: Session = Depends(get_db)):
    return tech_category_service.find_users_by_paged(db, page_param.offset, page_param.limit)


@router.post("/tech-categories", response_model=TechCategory, status_code=status.HTTP_201_CREATED)
async def create_new_tech_category(tech_category: RegisterTechCategory, db: Session = Depends(get_db)):
    find_tech_category = tech_category_service.find_tech_category_by_name(db, tech_category.name)
    if find_tech_category:
        raise DuplicateTechCategoryName(tech_category.name)
    return tech_category_service.create_tech_category(db, tech_category)


@router.get("/tech-categories/{tech_category_id}", response_model=TechCategory)
async def get_tech_category(tech_category_id: int, db: Session = Depends(get_db)):
    find_tech_category = tech_category_service.find_tech_category_by_id(db, tech_category_id)
    if not find_tech_category:
        raise NotFound()
    return find_tech_category


@router.put("/tech-categories/{tech_category_id}", response_model=TechCategory, status_code=status.HTTP_200_OK)
async def change_tech_category(tech_category_id: int,
                               tech_category: RegisterTechCategory,
                               db: Session = Depends(get_db)):
    return tech_category_service.update_tech_category(db, tech_category_id, tech_category)


@router.delete("/tech-categories/{tech_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tech_category(tech_category_id: int, db: Session = Depends(get_db)):
    tech_category_service.delete_tech_category(db, tech_category_id)
