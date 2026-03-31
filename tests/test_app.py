from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"] == activities["Chess Club"]["description"]
    assert isinstance(payload["Chess Club"]["participants"], list)
