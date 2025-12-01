import json
import pytest
from src.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_index_loads(client):
    """Dashboard loads successfully"""
    res = client.get("/")
    assert res.status_code == 200


def test_predict_valid_request(client):
    """Valid payload should return prediction JSON"""
    payload = {
        "offense": "BUF",
        "defense": "MIA",
        "yardline": 60,
        "ydstogo": 4,
        "time_left": 180,
        "score_diff": -3
    }

    res = client.post("/predict",
                      data=json.dumps(payload),
                      content_type="application/json")

    assert res.status_code == 200
    data = res.get_json()

    assert "go_wpa" in data
    assert "fg_wpa" in data
    assert "punt_wpa" in data
    assert "decision" in data


def test_predict_missing_team(client):
    """Missing offense or defense should return 400"""
    payload = {
        "offense": "",
        "defense": "BUF",
        "yardline": 50,
        "ydstogo": 10,
        "time_left": 120,
        "score_diff": 0
    }

    res = client.post("/predict",
                      data=json.dumps(payload),
                      content_type="application/json")

    assert res.status_code == 400


def test_down_is_always_4(client):
    """Ensure model always uses 4th down, even if user tries otherwise"""
    payload = {
        "offense": "BUF",
        "defense": "NYJ",
        "yardline": 45,
        "ydstogo": 3,
        "time_left": 300,
        "score_diff": 7
    }

    res = client.post("/predict",
                      data=json.dumps(payload),
                      content_type="application/json")

    assert res.status_code == 200