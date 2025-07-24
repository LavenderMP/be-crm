# test_users.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.models.event import Event, EventAttendance
from app.tests.test_data import TEST_USERS, create_test_data

client = TestClient(app)

def test_get_users_no_filters(db: Session):
    # Setup
    for user_data in TEST_USERS:
        db.add(User(**user_data))
    db.commit()
    
    # Test
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_filter_by_company(db: Session):
    # Test
    response = client.get("/users?company=TechCorp")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(user["company"] == "TechCorp" for user in data)

def test_filter_by_state(db: Session):
    response = client.get("/users?state=CA")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(user["state"] == "CA" for user in data)

def test_filter_by_city(db: Session):
    response = client.get("/users?city=San Francisco")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["city"] == "San Francisco"

def test_pagination(db: Session):
    # Add more users
    for i in range(15):
        user_data = {
            "first_name": f"User{i}",
            "last_name": f"Test",
            "email": f"user{i}@example.com",
            "company": f"Company{i}",
            "city": "Test City",
            "state": "TS"
        }
        db.add(User(**user_data))
    db.commit()
    
    # Test pagination
    response = client.get("/users?page=2&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["first_name"] == "User5"

def test_sorting(db: Session):
    response = client.get("/users?sort_by=first_name&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    first_names = [user["first_name"] for user in data]
    assert first_names == sorted(first_names, reverse=True)

def test_event_counts(db: Session):
    # Create test data including events and relationships
    test_data = create_test_data(db)
    
    # Access specific test data
    john = next(u for u in test_data["users"] if u.email == "john@techcorp.com")
    
    # Test counts
    response = client.get(f"/users/{john.id}")
    data = response.json()
    
    assert data["hosted_events_count"] == 1  # John owns event1
    assert data["attended_events_count"] == 1  # John attended event1