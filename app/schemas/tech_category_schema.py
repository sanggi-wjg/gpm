from datetime import datetime

from pydantic import BaseModel, PositiveInt


class RegisterTechCategory(BaseModel):
    name: str


class TechCategory(RegisterTechCategory):
    id: PositiveInt
    name: str
    datetime_of_created: datetime
    datetime_of_updated: datetime

    class Config:
        orm_mode = True
