from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/h")
    assert response.status_code == 200
    assert response.json() == {"status": "good"}

def test_list_appointments():
    response = client.get("/appointment")
    assert response.status_code == 200
    assert response.json() == {"appointments": []}
