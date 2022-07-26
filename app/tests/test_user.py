from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.repositories import user_repo
from app.schemas.user_schema import RegisterUser, User


class TestUserRepo:

    def setup_method(self, method):
        pass

    def test_create_new_user(self, test_db: Session):
        register_user = RegisterUser(
            email="test@host.com",
            password1="123", password2="123"
        )
        new_user = user_repo.create_user(test_db, register_user)
        assert new_user.id == 1
        assert new_user.email == "test@host.com"

    def test_find_user_by_email(self, test_db: Session):
        is_exist = user_repo.is_exist_user_by_email(test_db, "123")
        assert not is_exist


class TestUserRouter:

    def setup_method(self, method):
        self.url = {
            'user-list': '/users'
        }

    def test_get_users(self, app: FastAPI, test_db: Session, client: TestClient):
        response = client.get(self.url.get('user-list'))
        assert response.status_code == status.HTTP_200_OK

    def test_post_users(self, app: FastAPI, test_db: Session, client: TestClient):
        # given
        register_user = RegisterUser(
            email="test@host.com",
            password1="123", password2="123"
        )
        # when
        response = client.post(self.url.get('user-list'), json=jsonable_encoder(register_user))
        data = response.json()
        user = User(**data)

        # then
        assert response.status_code == status.HTTP_201_CREATED
        assert user
