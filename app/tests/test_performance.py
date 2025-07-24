# test_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.models.campaign import EmailCampaign

client = TestClient(app)


@pytest.mark.stresstest
def test_large_dataset_performance(db: Session):
    # Create 1000 users
    for i in range(1000):
        user = User(
            first_name=f"User{i}",
            last_name="Stress",
            email=f"user{i}@test.com",
            company=f"Company{i%10}",
            state=f"ST{i%5}",
        )
        db.add(user)
    db.commit()

    # Test query performance
    start_time = time.time()
    response = client.get("/users?company=Company5&state=ST3")
    duration = time.time() - start_time

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert duration < 0.5  # Should be under 500ms


def test_invalid_filters(db: Session):
    response = client.get("/users?invalid_param=value")
    assert response.status_code == 422  # Unprocessable Entity


def test_out_of_range_pagination(db: Session):
    response = client.get("/users?page=100&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_email_campaign_failure(db: Session, mocker):
    # Mock email sending to fail
    mocker.patch("main.send_single_email", side_effect=Exception("SMTP error"))

    payload = {
        "filters": {"email": "john@techcorp.com"},
        "subject": "Test Failure",
        "body": "This should fail",
    }
    response = client.post("/send_emails", json=payload)
    campaign_id = response.json()["campaign_id"]

    # Process campaign
    from main import process_email_campaign

    process_email_campaign(campaign_id)

    campaign = db.query(EmailCampaign).get(campaign_id)
    assert campaign.status == "failed"
