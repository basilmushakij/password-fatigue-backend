"""Small tests for the API. Run from the backend/ folder:  python -m pytest -q"""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_returns_risk_level_and_features():
    r = client.post("/predict", json={"password": "qwerty123"})
    assert r.status_code == 200
    body = r.json()
    assert body["risk_level"] in (0, 1, 2)
    assert body["avg_dist"] >= 0
    assert 0 < body["unique_ratio"] <= 1


def test_empty_password_is_rejected():
    r = client.post("/predict", json={"password": ""})
    assert r.status_code == 422


def test_too_long_password_is_rejected():
    r = client.post("/predict", json={"password": "a" * 129})
    assert r.status_code == 422


def test_missing_field_is_rejected():
    r = client.post("/predict", json={})
    assert r.status_code == 422


def test_cors_only_allows_the_demo_frontend():
    ok = client.get("/health", headers={"Origin": "http://localhost:4000"})
    assert ok.headers.get("access-control-allow-origin") == "http://localhost:4000"
    other = client.get("/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in other.headers
