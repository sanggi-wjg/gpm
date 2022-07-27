from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.service import user_service
from app.schemas.user_schema import UserRegister


def get_access_token_for_test(client: TestClient, test_db: Session, email: str, password: str):
    register_user = UserRegister(email=email, password1=password, password2=password)
    user_service.create_user(test_db, register_user)

    response = client.post("/login", jsonable_encoder({"username": email, "password": password}))
    access_token = response.json()['access_token']
    return {
        "Authorization": f"Bearer {access_token}"
    }
