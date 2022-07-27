import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class UserStatus(enum.Enum):
    ACTIVE = "Active"
    STOP = "Stop"
    DROP = "Drop"


class UserEntity(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)

    email = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(250), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)

    datetime_of_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    datetime_of_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class TechCategoryEntity(Base):
    __tablename__ = 'tech_category'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    # 역방향 relation
    tech_stacks = relationship("TechStackEntity", back_populates="tech_category")

    datetime_of_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    datetime_of_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class TechStackEntity(Base):
    __tablename__ = 'tech_stack'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    name = Column(String(50), nullable=False, index=True)

    # 정방향 relation
    tech_category_id = Column(Integer, ForeignKey("tech_category.id"), nullable=False)
    tech_category = relationship("TechCategoryEntity", back_populates="tech_stacks")

    datetime_of_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    datetime_of_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
