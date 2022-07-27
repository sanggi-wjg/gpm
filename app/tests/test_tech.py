from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from app.service import tech_service
from app.schemas.tech_schema import TechCategory, RegisterTechCategory


class TestTechCategoryRepo:

    def setup_method(self, method):
        pass

    def test_create_new_tech_category(self, test_db: Session):
        category_name = "Programming Language"
        register_tech_category = RegisterTechCategory(name=category_name)

        new_tech_category = tech_service.create_tech_category(test_db, register_tech_category)

        assert new_tech_category.id == 1
        assert new_tech_category.name == category_name


class TestTechCategoryRouter:

    def setup_method(self, method):
        self.url = '/api/v1/tech-categories'

    def test_get_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        # given
        category_name = "Programming Language"
        # when
        response = client.post(self.url, json=jsonable_encoder(RegisterTechCategory(name=category_name)))
        data = response.json()
        tech_category = TechCategory(**data)
        # then
        assert response.status_code == status.HTTP_201_CREATED
        assert tech_category
        assert tech_category.id == 1
        assert tech_category.name == category_name


class TestTechCategoryDetailRouter:

    def get_url(self, client: TestClient):
        url = "/api/v1/tech-categories"

        response = client.post(url, json=jsonable_encoder(RegisterTechCategory(name="Programming Language")))
        tech_category = TechCategory(**response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert tech_category.id == 1

        return f"{url}/{tech_category.id}"

    def test_get_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        response = client.get(self.get_url(client))
        assert response.status_code == status.HTTP_200_OK

    def test_put_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        # given
        change_name = "Framework"
        # when
        response = client.put(self.get_url(client), json=jsonable_encoder(RegisterTechCategory(name=change_name)))
        tech_category = TechCategory(**response.json())
        find_tech_category = tech_service.find_tech_category_by_id(test_db, 1)
        # then
        assert response.status_code == status.HTTP_200_OK
        assert tech_category.name == change_name
        assert find_tech_category.name == change_name

    def test_delete_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        # given
        # when
        response = client.delete(self.get_url(client))
        find_tech_category = tech_service.find_tech_category_by_id(test_db, 1)
        # then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not find_tech_category
