from typing import List

from pydantic import BaseModel, PositiveInt


class TechStackBase(BaseModel):
    id: PositiveInt
    name: str
    # badge: str
    # datetime_of_created: datetime
    # datetime_of_updated: datetime


class TechStackRegister(BaseModel):
    name: str
    color: str | None = ''

    # @validator("color")
    # def replace_color(cls, color):
    #     if color:
    #         color = color.replace(" ", '')
    #     return color


class TechStack(TechStackBase):
    tech_category_id: PositiveInt

    class Config:
        orm_mode = True


class TechCategoryBase(BaseModel):
    id: PositiveInt
    name: str
    # datetime_of_created: datetime
    # datetime_of_updated: datetime


class TechCategoryRegister(BaseModel):
    name: str


class TechCategory(TechCategoryBase):
    tech_stacks: List[TechStack] = []

    class Config:
        orm_mode = True
