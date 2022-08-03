from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from app.schemas.user_schema import UserRegister
from app.service import user_service


class TestAuthRouter:

    # def setup_method(self, method):
    #     self.url = '/api/v1/users'

    def test_get_login_page(self, client: TestClient):
        response = client.get("/login")
        assert response.status_code == status.HTTP_200_OK

    def test_get_login_github_page(self, client: TestClient):
        response = client.get("/login/github", allow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    def test_post_token(self, test_db: Session, client: TestClient, access_token_headers):
        # given
        user_email, password = "test@host.com", "123"
        user_register = UserRegister(email=user_email, password1=password, password2=password)
        _ = user_service.create_admin_user(test_db, user_register)
        # when
        response = client.post("/token", jsonable_encoder({"username": user_email, "password": password}))
        # then
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['access_token']

    def test_post_token_invalid_user(self, test_db: Session, client: TestClient, access_token_headers):
        # given
        user_email, password = "test@host.com", "123"
        user_register = UserRegister(email=user_email, password1=password, password2=password)
        _ = user_service.create_admin_user(test_db, user_register)
        # when
        response = client.post("/token", jsonable_encoder({"username": user_email, "password": password + "1"}))
        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
