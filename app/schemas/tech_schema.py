from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveInt


class RegisterTechStack(BaseModel):
    name: str


class TechStack(RegisterTechStack):
    id: PositiveInt
    name: str
    datetime_of_created: datetime
    datetime_of_updated: datetime

    class Config:
        orm_mode = True


class RegisterTechCategory(BaseModel):
    name: str


class TechCategory(RegisterTechCategory):
    id: PositiveInt
    name: str
    datetime_of_created: datetime
    datetime_of_updated: datetime
    tech_stacks: List[TechStack] = []

    class Config:
        orm_mode = True
