"""Smoke tests for NovaSphere."""

from fastapi.testclient import TestClient

from src.main import app


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_index() -> None:
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "NovaSphere" in r.text


def test_history_empty() -> None:
    client = TestClient(app)
    r = client.get("/history")
    assert r.status_code == 200
    assert r.json()["count"] == 0
