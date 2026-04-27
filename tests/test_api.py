from fastapi.testclient import TestClient
from app.api import app


def test_health():
    client = TestClient(app)
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json()['status'] == 'ok'


def test_metrics():
    client = TestClient(app)
    res = client.get('/metrics')
    assert res.status_code == 200
    assert 'total_requests' in res.json()
