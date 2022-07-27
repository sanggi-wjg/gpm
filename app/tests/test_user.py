from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.service import user_service
from app.schemas.user_schema import User, RegisterUser


class TestUserRepo:

    def setup_method(self, method):
        pass

    def test_create_new_user(self, test_db: Session):
        register_user = RegisterUser(
            email="test@host.com",
            password1="123",
            password2="123"
        )
        new_user = user_service.create_user(test_db, register_user)
        assert new_user.id == 1
        assert new_user.email == "test@host.com"


class TestUserRouter:

    def setup_method(self, method):
        self.url = '/api/v1/users'

    def test_get_users(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        response = client.get(self.url, headers=access_token_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_post_users(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        # given
        register_user = RegisterUser(
            email="test@host.com",
            password1="123",
            password2="123",
        )
        # when
        response = client.post(self.url, json=jsonable_encoder(register_user), headers=access_token_headers)
        data = response.json()
        user = User(**data)
        # then
        assert response.status_code == status.HTTP_201_CREATED
        assert user
