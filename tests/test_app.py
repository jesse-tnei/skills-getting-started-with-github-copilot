import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: GET /activities

def test_get_activities():
    # Arrange
    # (TestClient already arranged)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test: POST /activities/{activity_name}/signup (success)

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Confirm participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

# Test: POST /activities/{activity_name}/signup (duplicate)

def test_signup_for_activity_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]

# Test: DELETE /activities/{activity_name}/signup (success)

def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Confirm participant removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]

# Test: DELETE /activities/{activity_name}/signup (not found)

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# Test: POST /activities/{activity_name}/signup (invalid activity)

def test_signup_invalid_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
