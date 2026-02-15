from fastapi.testclient import TestClient
from src.main import app
from io import BytesIO

client = TestClient(app)

def test_srs_upload():
    # Create a dummy PDF in memory
    dummy_pdf = BytesIO(b"%PDF-1.4\n%Dummy PDF for testing\n")
    files = {"file": ("sample_srs.pdf", dummy_pdf, "application/pdf")}

    response = client.post("/upload-srs", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert data["filename"] == "sample_srs.pdf"
