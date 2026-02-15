from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_requirement_extraction():
    response = client.get("/requirements/1")
    assert response.status_code == 200
   
    data = response.json()
    assert "id" in data
    assert data["id"] == 1