import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.database.database import Base


class UserStatus(enum.Enum):
    ACTIVE = "Active"
    STOP = "Stop"
    DROP = "Drop"


class UserEntity(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True, autoincrement = "auto", index = True)

    email = Column(String(50), unique = True, nullable = False, index = True)
    hashed_password = Column(String(250), nullable = False)
    status = Column(Enum(UserStatus), nullable = False, default = UserStatus.ACTIVE)

    datetime_of_created = Column(DateTime(timezone = True), default=datetime.utcnow)
    datetime_of_updated = Column(DateTime(timezone = True), default=datetime.utcnow, onupdate=datetime.utcnow)
