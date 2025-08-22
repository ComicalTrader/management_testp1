from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime

client = TestClient(app)

def test_create_finance():
    payload = {
        "description": "Venda de produto",
        "amount": 100.0,
        "type": "income",
        "date": datetime.now().isoformat()
    }
    response = client.post("/finance/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Venda de produto"
    assert "id" in data

def test_list_finances():
    response = client.get("/finance/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
