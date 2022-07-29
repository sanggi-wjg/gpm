from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from app.service import tech_service
from app.schemas.tech_schema import TechCategory, TechCategoryRegister, TechStackRegister


class TestTechCategoryRepo:

    def setup_method(self, method):
        pass

    def test_create_new_tech_category(self, test_db: Session):
        category_name = "Programming Language"
        register_tech_category = TechCategoryRegister(name=category_name)

        new_tech_category = tech_service.create_tech_category(test_db, register_tech_category)

        assert new_tech_category.id == 1
        assert new_tech_category.name == category_name


class TestTechCategoryRouter:

    def setup_method(self, method):
        self.url = '/api/v1/tech-categories'

    def test_get_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        # given
        category_name = "Programming Language"
        # when
        response = client.post(self.url,
                               json=jsonable_encoder(TechCategoryRegister(name=category_name)),
                               headers=access_token_headers)
        data = response.json()
        tech_category = TechCategory(**data)
        # then
        assert response.status_code == status.HTTP_201_CREATED
        assert tech_category
        assert tech_category.id == 1
        assert tech_category.name == category_name

    def test_post_tech_categories_duplicate(self, app: FastAPI, test_db: Session, client: TestClient,
                                            access_token_headers):
        # given
        category_name = "Programming Language"
        response = client.post(self.url,
                               json=jsonable_encoder(TechCategoryRegister(name=category_name)),
                               headers=access_token_headers)
        assert response.status_code == status.HTTP_201_CREATED
        # when
        category_name = "Programming Language"
        response = client.post(self.url,
                               json=jsonable_encoder(TechCategoryRegister(name=category_name)),
                               headers=access_token_headers)
        # then
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestTechCategoryDetailRouter:

    def get_url(self, client: TestClient, access_token_headers):
        url = "/api/v1/tech-categories"

        response = client.post(url,
                               json=jsonable_encoder(TechCategoryRegister(name="Programming Language")),
                               headers=access_token_headers)
        tech_category = TechCategory(**response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert tech_category.id == 1

        return f"{url}/{tech_category.id}"

    def test_get_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        response = client.get(self.get_url(client, access_token_headers))
        assert response.status_code == status.HTTP_200_OK

    def test_put_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        # given
        change_name = "Framework"
        # when
        response = client.put(self.get_url(client, access_token_headers),
                              json=jsonable_encoder(TechCategoryRegister(name=change_name)),
                              headers=access_token_headers)
        tech_category = TechCategory(**response.json())
        find_tech_category = tech_service.find_tech_category_by_id(test_db, 1)
        # then
        assert response.status_code == status.HTTP_200_OK
        assert tech_category.name == change_name
        assert find_tech_category.name == change_name

    def test_delete_tech_categories(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        # given
        # when
        response = client.delete(self.get_url(client, access_token_headers), headers=access_token_headers)
        find_tech_category = tech_service.find_tech_category_by_id(test_db, 1)
        # then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not find_tech_category


class TestTechStackRouter:

    def get_url(self, client: TestClient, access_token_headers):
        url = "/api/v1/tech-categories"

        response = client.post(url,
                               json=jsonable_encoder(TechCategoryRegister(name="Programming Language")),
                               headers=access_token_headers)
        tech_category = TechCategory(**response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert tech_category.id == 1

        return f"{url}/{tech_category.id}/tech-stacks"

    def test_post_tech_stacks(self, app: FastAPI, test_db: Session, client: TestClient, access_token_headers):
        # given
        stack_name = "Python"
        # when
        response = client.post(self.get_url(client, access_token_headers),
                               json=jsonable_encoder(TechStackRegister(name=stack_name)),
                               headers=access_token_headers)
        # then
        assert response.status_code == status.HTTP_201_CREATED
