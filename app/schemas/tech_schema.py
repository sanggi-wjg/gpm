from typing import List

from pydantic import BaseModel, PositiveInt, validator


class TechStackBase(BaseModel):
    id: PositiveInt


class TechStackRegister(BaseModel):
    name: str
    color: str | None = None

    @validator("color")
    def replace_color(cls, color):
        if color:
            color = color.replace(" ", '')
        return color


class TechStack(TechStackBase):
    name: str
    tech_category_id: PositiveInt
    color: str | None = None

    class Config:
        orm_mode = True


class TechCategoryBase(BaseModel):
    id: PositiveInt


class TechCategoryRegister(BaseModel):
    name: str


class TechCategory(TechCategoryBase):
    name: str
    tech_stacks: List[TechStack] = []

    class Config:
        orm_mode = True
