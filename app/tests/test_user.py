from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.database.models import UserProvider, UserStatus
from app.service import user_service
from app.schemas.user_schema import UserRegister


class TestUserRepo:

    def setup_method(self, method):
        pass

    def test_create_normal_user(self, test_db: Session):
        # given
        user_email = "test@host.com"
        user_register = UserRegister(email=user_email, password1="123", password2="123")
        # when
        new_user = user_service.create_user(test_db, user_register)
        # then
        assert new_user.id == 1
        assert new_user.email == user_email
        assert new_user.is_admin is False
        assert new_user.provider == UserProvider.OWN

    def test_create_super_user(self, test_db: Session):
        # given
        user_email = "test@host.com"
        user_register = UserRegister(email=user_email, password1="123", password2="123")
        # when
        new_user = user_service.create_admin_user(test_db, user_register)
        # then
        assert new_user.id == 1
        assert new_user.email == user_email
        assert new_user.is_admin is True
        assert new_user.provider == UserProvider.OWN


class TestUserRouter:

    def setup_method(self, method):
        self.url = '/api/v1/users'

    def test_get_users_with_normal_user(self, app: FastAPI, test_db: Session, client: TestClient,
                                        access_token_headers):
        # when
        response = client.get(self.url, headers=access_token_headers)
        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_with_admin_user(self, app: FastAPI, test_db: Session, client: TestClient,
                                       access_token_headers_admin):
        # when
        response = client.get(self.url, headers=access_token_headers_admin)
        # then
        assert response.status_code == status.HTTP_200_OK

    def test_post_users_with_normal_user(self, app: FastAPI, test_db: Session, client: TestClient,
                                         access_token_headers):
        # given
        register_user = UserRegister(email="test@host.com", password1="123", password2="123")
        # when
        response = client.post(self.url, json=jsonable_encoder(register_user), headers=access_token_headers)
        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_users_with_admin_user(self, app: FastAPI, test_db: Session, client: TestClient,
                                        access_token_headers_admin):
        # given
        user_email = "test@host.com"
        register_user = UserRegister(email=user_email, password1="123", password2="123")
        # when
        response = client.post(self.url, json=jsonable_encoder(register_user), headers=access_token_headers_admin)
        # then
        assert response.status_code == status.HTTP_201_CREATED
        # then
        find_user = user_service.find_user_by_email(test_db, user_email)
        assert find_user.id == 2
        assert find_user.email == user_email
        assert find_user.is_admin is False
        assert find_user.status == UserStatus.ACTIVE
        assert find_user.provider == UserProvider.OWN

    def test_post_users_duplicate_with_admin_user(self, app: FastAPI, test_db: Session, client: TestClient,
                                                  access_token_headers_admin):
        # given
        user_email = "test@host.com"
        register_user = UserRegister(email=user_email, password1="123", password2="123")
        # when
        response = client.post(self.url, json=jsonable_encoder(register_user), headers=access_token_headers_admin)
        # then
        assert response.status_code == status.HTTP_201_CREATED
        del response
        # then
        response = client.post(self.url, json=jsonable_encoder(register_user), headers=access_token_headers_admin)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
