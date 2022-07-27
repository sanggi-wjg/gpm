from typing import List

from sqlalchemy.orm import Session

from app.database.models import TechCategoryEntity, TechStackEntity
from app.exceptions.exception import NotFound
from app.schemas.tech_schema import RegisterTechCategory


def find_tech_categories_by_paged(db: Session, offset: int, limit: int) -> List[TechCategoryEntity]:
    return db.query(TechCategoryEntity).offset(offset).limit(limit).all()


def find_tech_category_by_name(db: Session, name: str) -> TechCategoryEntity:
    return db.query(TechCategoryEntity).filter(TechCategoryEntity.name == name).first()


def find_tech_category_by_id(db: Session, tech_category_id: int) -> TechCategoryEntity:
    return db.query(TechCategoryEntity).filter(TechCategoryEntity.id == tech_category_id).first()


def create_tech_category(db: Session, tech_category: RegisterTechCategory) -> TechCategoryEntity:
    new_tech_category = TechCategoryEntity(name=tech_category.name)
    db.add(new_tech_category)
    db.commit()
    db.refresh(new_tech_category)
    return new_tech_category


def update_tech_category(db: Session, tech_category_id: int, tech_category: RegisterTechCategory) -> TechCategoryEntity:
    find_tech_category = find_tech_category_by_id(db, tech_category_id)
    if not find_tech_category:
        raise NotFound()

    find_tech_category.update(tech_category.name)

    db.commit()
    db.refresh(find_tech_category)
    return find_tech_category


def delete_tech_category(db: Session, tech_category_id: int):
    find_tech_category = find_tech_category_by_id(db, tech_category_id)
    if not find_tech_category:
        raise NotFound()

    db.delete(find_tech_category)
    db.commit()
    return True


def find_tech_stacks_by_paged(db: Session, offset: int, limit: int) -> List[TechStackEntity]:
    return db.query(TechStackEntity).offset(offset).limit(limit).all()
