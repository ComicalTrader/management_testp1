from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime

client = TestClient(app)

def test_create_appointment():
    payload = {
        "customer_name": "João",
        "phone": "123456789",
        "service": "Corte",
        "start_at": datetime.now().isoformat(),
        "notes": "Teste"
    }
    response = client.post("/appointment/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "João"
    assert "id" in data

def test_list_appointments():
    response = client.get("/appointment/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
