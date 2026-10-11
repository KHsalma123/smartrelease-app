from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_returns_v1():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["project"] == "SmartRelease"
    assert response.json()["version"] == "v1"
    assert response.json()["status"] == "healthy"


def test_health_returns_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
