# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20))
    email = Column(String(100), unique=True, index=True, nullable=False)
    avatar = Column(String(200))
    gender = Column(String(10))
    job_title = Column(String(100))
    company = Column(String(100), index=True)
    city = Column(String(50), index=True)
    state = Column(String(50), index=True)

    # Relationships
    hosted_events = relationship("Event", back_populates="owner")
    event_attendances = relationship("EventAttendance", back_populates="user")
