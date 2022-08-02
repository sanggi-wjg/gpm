from typing import Generator, Any

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from app.core.config import get_config_settings
from app.database.database import Base, get_db
from app.main import create_app
from app.tests.utils.test_utils import get_access_token_for_normal_user, get_access_token_for_admin_user

"""
https://github.com/timhughes/example-fastapi-sqlachemy-pytest/blob/master/tests/conftest.py
"""

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)
testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
settings = get_config_settings()


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    yield create_app()
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_db(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = testingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(app: FastAPI, test_db: Session) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def access_token_headers(client: TestClient, test_db: Session):
    return get_access_token_for_normal_user(client, test_db, settings.test_user_email, settings.test_user_password)


@pytest.fixture
def access_token_headers_admin(client: TestClient, test_db: Session):
    return get_access_token_for_admin_user(client, test_db, settings.test_user_email, settings.test_user_password)
