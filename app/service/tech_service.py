from typing import List

from sqlalchemy.orm import Session

from app.database.models import TechCategoryEntity, TechStackEntity
from app.exceptions.exception import NotFound
from app.schemas.tech_schema import TechStackRegister, TechCategoryRegister


def find_tech_category_all_by_paged(db: Session, offset: int, limit: int) -> List[TechCategoryEntity]:
    return db.query(TechCategoryEntity).offset(offset).limit(limit).all()


def find_tech_category_by_name(db: Session, name: str) -> TechCategoryEntity:
    return db.query(TechCategoryEntity).filter(TechCategoryEntity.name == name).first()


def find_tech_category_by_id(db: Session, tech_category_id: int) -> TechCategoryEntity:
    return db.query(TechCategoryEntity).filter(TechCategoryEntity.id == tech_category_id).first()


def create_tech_category(db: Session, tech_category: TechCategoryRegister) -> TechCategoryEntity:
    new_tech_category = TechCategoryEntity(name=tech_category.name)
    db.add(new_tech_category)
    db.commit()
    db.refresh(new_tech_category)
    return new_tech_category


def find_tech_category_by_id_or_not_found(db: Session, tech_category_id: int):
    find_tech_category = find_tech_category_by_id(db, tech_category_id)
    if not find_tech_category:
        raise NotFound()
    return find_tech_category


def update_tech_category(db: Session, tech_category_id: int, tech_category: TechCategoryRegister) -> TechCategoryEntity:
    find_tech_category = find_tech_category_by_id_or_not_found(db, tech_category_id)
    find_tech_category.update(tech_category.name)

    db.commit()
    db.refresh(find_tech_category)
    return find_tech_category


def delete_tech_category(db: Session, tech_category_id: int):
    find_tech_category = find_tech_category_by_id_or_not_found(db, tech_category_id)

    db.delete(find_tech_category)
    db.commit()
    return True


def find_tech_stack_all_by_paged(db: Session, tech_category_id: int, offset: int, limit: int) -> List[TechStackEntity]:
    return db.query(TechStackEntity).filter(
        TechStackEntity.tech_category_id == tech_category_id
    ).offset(offset).limit(limit).all()


def create_tech_stack(db: Session, tech_category_id: int, tech_stack: TechStackRegister):
    find_tech_category = find_tech_category_by_id_or_not_found(db, tech_category_id)
    new_tech_stack = TechStackEntity(name=tech_stack.name, tech_category_id=find_tech_category.id)

    db.add(new_tech_stack)
    db.commit()
    db.refresh(new_tech_stack)
    return new_tech_stack