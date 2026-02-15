from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_testcase_generation():
    response = client.post("/generate-tests/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "testcases" in data