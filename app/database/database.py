from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_config_settings


def create_database_engine():
    settings = get_config_settings()
    match settings.database_engine:
        case "MYSQL":
            return create_engine(
                settings.mysql_dsn,
                isolation_level='REPEATABLE READ',
                pool_size=100,
                max_overflow=200,
                echo=False
            )
        case "SQLITE":
            database_dsn = "sqlite:///:memory:"
            return create_engine(database_dsn, connect_args={"check_same_thread": False})
        case _:
            raise Exception(f"check database dsn:{settings.database_engine}")


Engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
