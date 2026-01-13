from fastapi.testclient import TestClient
from api.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_prediction_low_risk(client):
    data = {
        "gender": 1,
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 0,
        "tenure": 12,
        "PhoneService": 1,
        "PaperlessBilling": 1,
        "MonthlyCharges": 70.5,
        "TotalCharges": 850.0
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "churn_prediction" in response.json()
    assert "churn_probability" in response.json()
    assert "risk_level" in response.json()

def test_prediction_high_risk(client):
    data = {
        "gender": 0,
        "SeniorCitizen": 1,
        "Partner": 0,
        "Dependents": 0,
        "tenure": 1,
        "PhoneService": 1,
        "PaperlessBilling": 1,
        "MonthlyCharges": 100.0,
        "TotalCharges": 100.0
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
