import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)


def test_signup_rejects_duplicate_registration():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": " Michael@Mergington.edu "},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert activities["Chess Club"]["participants"].count("michael@mergington.edu") == 1


def test_signup_allows_new_registration():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
