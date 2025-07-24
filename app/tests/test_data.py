from datetime import datetime, timedelta
from app.models.user import User
from app.models.event import Event, EventAttendance
from app.models.campaign import EmailCampaign


TEST_USERS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@techcorp.com",
        "company": "TechCorp",
        "job_title": "Engineer",
        "city": "San Francisco",
        "state": "CA"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@innovateinc.com",
        "company": "InnovateInc",
        "job_title": "Manager",
        "city": "New York",
        "state": "NY"
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob@techcorp.com",
        "company": "TechCorp",
        "job_title": "Director",
        "city": "Los Angeles",
        "state": "CA"
    }
]

TEST_EVENTS = [
    {
        "slug": "tech-summit-2023",
        "title": "Annual Tech Summit",
        "start_at": "2023-10-15T09:00:00",
        "end_at": "2023-10-17T18:00:00",
        "venue": "Moscone Center",
        "max_capacity": 1000
    }
]


# Helper function to create test relationships
def create_test_data(db):
    # Create test users
    user1 = User(
        first_name="John",
        last_name="Doe",
        email="john@techcorp.com",
        company="TechCorp",
        job_title="Engineer",
        city="San Francisco",
        state="CA",
    )

    user2 = User(
        first_name="Jane",
        last_name="Smith",
        email="jane@innovateinc.com",
        company="InnovateInc",
        job_title="Manager",
        city="New York",
        state="NY",
    )

    user3 = User(
        first_name="Bob",
        last_name="Johnson",
        email="bob@techcorp.com",
        company="TechCorp",
        job_title="Director",
        city="Los Angeles",
        state="CA",
    )

    db.add_all([user1, user2, user3])
    db.commit()

    # Create test events
    event1 = Event(
        slug="tech-summit-2023",
        title="Annual Tech Summit",
        description="The biggest tech event of the year",
        start_at=datetime.now() + timedelta(days=10),
        end_at=datetime.now() + timedelta(days=12),
        venue="Moscone Center",
        max_capacity=1000,
        owner_id=user1.id,
    )

    event2 = Event(
        slug="dev-conference",
        title="Developers Conference",
        description="For developers by developers",
        start_at=datetime.now() + timedelta(days=20),
        end_at=datetime.now() + timedelta(days=22),
        venue="Convention Center",
        max_capacity=500,
        owner_id=user2.id,
    )

    db.add_all([event1, event2])
    db.commit()

    # Create event relationships
    attendance1 = EventAttendance(event_id=event1.id, user_id=user1.id, attended=True)

    attendance2 = EventAttendance(event_id=event1.id, user_id=user2.id, attended=True)

    attendance3 = EventAttendance(
        event_id=event2.id,
        user_id=user3.id,
        attended=False,  # Registered but not attended yet
    )

    db.add_all([attendance1, attendance2, attendance3])
    db.commit()

    # Create test email campaign
    campaign = EmailCampaign(
        filters={"company": "TechCorp"},
        subject="Welcome TechCorp Employees",
        body="Special offers for you!",
        status="completed",
        sent_count=2,
        total_recipients=2,
    )

    db.add(campaign)
    db.commit()

    return {
        "users": [user1, user2, user3],
        "events": [event1, event2],
        "campaign": campaign,
    }
