from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_customer():
    payload = {
        "name": "Maria",
        "contact": "987654321",
        "notes": "Cliente VIP"
    }
    response = client.post("/customers/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Maria"
    assert "id" in data

def test_list_customers():
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
