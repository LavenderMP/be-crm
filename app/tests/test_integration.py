import pytest
from app.tests.test_data import TEST_USERS, TEST_EVENTS
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.campaign import EmailCampaign

client = TestClient(app)


# test_integration.py
def test_full_workflow(db: Session):
    # Create user
    user_data = TEST_USERS[0]
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Create event
    event_data = TEST_EVENTS[0]
    event_data["owner_id"] = user_id
    response = client.post("/events", json=event_data)
    assert response.status_code == 201
    event_id = response.json()["id"]

    # Register attendance
    attendance_data = {"user_id": user_id, "attended": True}
    response = client.post(f"/events/{event_id}/attendances", json=attendance_data)
    assert response.status_code == 201

    # Send email to attendees
    payload = {
        "filters": {"attended_events_min": 1},
        "subject": "Thanks for attending!",
        "body": "We appreciate your participation",
    }
    response = client.post("/send_emails", json=payload)
    assert response.status_code == 200
    campaign_id = response.json()["campaign_id"]

    # Verify email campaign
    campaign = db.query(EmailCampaign).get(campaign_id)
    assert campaign.total_recipients == 1
    assert campaign.sent_count == 1
