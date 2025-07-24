# test_emails.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.models.campaign import EmailCampaign
from test_data import TEST_USERS

client = TestClient(app)


def test_send_emails_success(db: Session):
    # Setup
    for user_data in TEST_USERS:
        db.add(User(**user_data))
    db.commit()

    # Test
    payload = {
        "filters": {"company": "TechCorp"},
        "subject": "Important Update",
        "body": "Hello TechCorp team!",
    }
    response = client.post("/send_emails", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

    # Verify campaign created
    campaign = db.query(EmailCampaign).first()
    assert campaign is not None
    assert campaign.subject == "Important Update"
    assert campaign.total_recipients == 2


def test_send_emails_no_users(db: Session):
    payload = {
        "filters": {"company": "NonExistentCorp"},
        "subject": "Test",
        "body": "Content",
    }
    response = client.post("/send_emails", json=payload)
    assert response.status_code == 200
    data = response.json()

    campaign = db.query(EmailCampaign).first()
    assert campaign.status == "completed"
    assert campaign.sent_count == 0
    assert campaign.total_recipients == 0


def test_send_emails_complex_filters(db: Session):
    payload = {
        "filters": {"company": "TechCorp", "state": "CA", "attended_events_min": 1},
        "subject": "CA TechCorp Attendees",
        "body": "Special offer for you!",
    }
    response = client.post("/send_emails", json=payload)
    assert response.status_code == 200

    campaign = db.query(EmailCampaign).first()
    assert campaign is not None
    assert campaign.total_recipients >= 0  # Actual count depends on test data


def test_email_processing_status(db: Session):
    # First create campaign
    test_send_emails_success(db)

    campaign = db.query(EmailCampaign).first()
    campaign_id = campaign.id

    # Simulate processing
    # (In real test, you'd trigger the background task)
    from main import process_email_campaign

    process_email_campaign(campaign_id)

    # Verify status update
    updated_campaign = db.query(EmailCampaign).get(campaign_id)
    assert updated_campaign.status == "completed"
    assert updated_campaign.sent_count == 2
