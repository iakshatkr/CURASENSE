import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from apps.api.main import app
from fastapi.testclient import TestClient

def test_triage_basic():
    client = TestClient(app)
    res = client.post("/api/v1/triage", json={"text": "fever and cough"})
    assert res.status_code == 200
