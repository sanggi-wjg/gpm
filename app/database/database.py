import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.config import get_config_settings

settings = get_config_settings()


def create_database_engine():
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

# simple way to create database
if settings.debug:
    Base.metadata.create_all(bind=Engine)
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def command_session_factory() -> Session:
    return SessionLocal()
