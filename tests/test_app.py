from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "test-student@mergington.edu"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
