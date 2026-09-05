from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Smart Placement Management System API is running" in response.json()["message"]
