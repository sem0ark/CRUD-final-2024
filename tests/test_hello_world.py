from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/test")
    assert response.status_code == 200
    assert response == "Success"
