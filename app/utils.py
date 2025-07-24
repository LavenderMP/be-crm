# tests/fake_data.py
from faker import Faker
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.event import Event, EventAttendance
from app.models.campaign import EmailCampaign

fake = Faker()

COMPANIES = [
    "TechCorp", "InnovateInc", "DataDriven", "FutureSystems", "CloudNexus",
    "QuantumLeap", "ByteCraft", "NexusLabs", "VisionaryTech", "AlphaSolutions"
]

JOB_TITLES = [
    "Software Engineer", "Product Manager", "Data Scientist", "DevOps Engineer",
    "UX Designer", "System Architect", "QA Tester", "Security Analyst",
    "Database Administrator", "Technical Writer"
]

CITIES_STATES = [
    ("San Francisco", "CA"), ("New York", "NY"), ("Austin", "TX"),
    ("Seattle", "WA"), ("Boston", "MA"), ("Chicago", "IL"),
    ("Denver", "CO"), ("Miami", "FL"), ("Portland", "OR"), ("Atlanta", "GA")
]

def generate_fake_users(db: Session, count=100):
    """Generate fake user data"""
    users = []
    for _ in range(count):
        city, state = random.choice(CITIES_STATES)
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number()[:10],
            email=fake.email(),
            avatar=fake.image_url(width=200, height=200),
            gender=random.choice(["Male", "Female", "Other"]),
            job_title=random.choice(JOB_TITLES),
            company=random.choice(COMPANIES),
            city=city,
            state=state
        )
        db.add(user)
        users.append(user)
    db.commit()
    return users

def generate_fake_events(db: Session, users: list, count=50):
    """Generate fake event data"""
    events = []
    for _ in range(count):
        # Random date within next year
        start_date = fake.date_time_between(start_date="now", end_date="+1y")
        duration = timedelta(hours=random.randint(1, 8))
        
        event = Event(
            slug=fake.slug(),
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3),
            start_at=start_date,
            end_at=start_date + duration,
            venue=fake.address(),
            max_capacity=random.randint(10, 1000),
            owner_id=random.choice(users).id
        )
        db.add(event)
        events.append(event)
    db.commit()
    return events

def generate_fake_attendances(db: Session, users: list, events: list):
    """Generate fake attendance records"""
    for event in events:
        # Get random attendees (30-80% of capacity)
        num_attendees = random.randint(
            int(event.max_capacity * 0.3), 
            int(event.max_capacity * 0.8)
        )
        
        for _ in range(num_attendees):
            user = random.choice(users)
            attendance = EventAttendance(
                event_id=event.id,
                user_id=user.id,
                attended=random.choices([True, False], weights=[0.8, 0.2])[0]
            )
            db.add(attendance)
    db.commit()

def generate_fake_campaigns(db: Session, users: list, count=10):
    """Generate fake email campaigns"""
    campaigns = []
    for _ in range(count):
        # Random filter criteria
        filters = {}
        if random.random() > 0.3:
            filters["company"] = random.choice(COMPANIES)
        if random.random() > 0.4:
            filters["state"] = random.choice([s for _, s in CITIES_STATES])
        if random.random() > 0.5:
            filters["hosted_events_min"] = random.randint(1, 5)
        
        campaign = EmailCampaign(
            filters=filters,
            subject=fake.sentence(nb_words=6),
            body=fake.paragraph(nb_sentences=5),
            status=random.choice(["pending", "processing", "completed", "failed"]),
            sent_count=random.randint(0, len(users)),
            total_recipients=random.randint(0, len(users))
        )
        db.add(campaign)
        campaigns.append(campaign)
    db.commit()
    return campaigns

def generate_all_fake_data(db: Session):
    """Generate complete fake dataset"""
    print("Generating fake users...")
    users = generate_fake_users(db, count=100)
    
    print("Generating fake events...")
    events = generate_fake_events(db, users, count=50)
    
    print("Generating fake attendances...")
    generate_fake_attendances(db, users, events)
    
    print("Generating fake campaigns...")
    campaigns = generate_fake_campaigns(db, users, count=10)
    
    print("Fake data generation complete!")
    return {
        "users": users,
        "events": events,
        "campaigns": campaigns
    }