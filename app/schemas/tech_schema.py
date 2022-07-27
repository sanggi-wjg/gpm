from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveInt


class TechStackRegister(BaseModel):
    name: str


class TechStack(TechStackRegister):
    id: PositiveInt
    name: str
    datetime_of_created: datetime
    datetime_of_updated: datetime

    # tech_category: 'TechCategory' = None

    class Config:
        orm_mode = True


class TechCategoryRegister(BaseModel):
    name: str


class TechCategory(TechCategoryRegister):
    id: PositiveInt
    name: str
    datetime_of_created: datetime
    datetime_of_updated: datetime
    tech_stacks: List[TechStack] = []

    class Config:
        orm_mode = True
