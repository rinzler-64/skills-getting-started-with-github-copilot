import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def activity_name():
    return "Chess Club"


@pytest.fixture
def restore_activity_participants(activity_name):
    original_participants = activities[activity_name]["participants"][:]
    yield
    activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity(
    client,
    activity_name,
    restore_activity_participants,
):
    # Arrange
    email = "student@example.com"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
