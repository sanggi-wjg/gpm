from starlette import status
from starlette.testclient import TestClient


class TestUserRouter:

    def test_get_profile_page(self, client: TestClient):
        response = client.get("/profiles")
        assert response.status_code == status.HTTP_200_OK
