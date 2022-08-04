from typing import List

from pydantic import BaseModel, PositiveInt, validator, Field


class TechStackBase(BaseModel):
    id: PositiveInt


class TechStackRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, title="Tech Stack Name")
    color: str | None = Field(None, min_length=0, max_length=20, title="Tech Stack background color of logo")

    @validator("color")
    def replace_color(cls, color):
        if color:
            color = color.replace(" ", '')
        return color


class TechStack(TechStackBase):
    name: str = Field(..., min_length=1, max_length=50, title="Tech Stack Name")
    color: str | None = Field(None, min_length=0, max_length=20, title="Tech Stack background color of logo")
    tech_category_id: PositiveInt

    class Config:
        orm_mode = True


class TechCategoryBase(BaseModel):
    id: PositiveInt


class TechCategoryRegister(BaseModel):
    # ... => require=True 와 동일한 뜻
    # ... 이 불편하면 자세를 고쳐앉고 default=Required 로 써도 된다.
    name: str = Field(..., min_length=1, max_length=50, title="Tech Category Name", example="Programming Langauge")


class TechCategory(TechCategoryBase):
    name: str = Field(..., min_length=1, max_length=50, title="Tech Category Name")
    tech_stacks: List[TechStack] = []

    class Config:
        orm_mode = True
